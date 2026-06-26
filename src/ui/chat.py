"""Chat UI — messages, input, streaming, citations.

All HTML uses INLINE STYLES because Streamlit's sanitizer strips class attributes.
"""

import streamlit as st

from src.artifacts.parser import parse_slash_command
from src.models import ChatMessage, SourceChunk
from src.retrieval.rag_chain import get_answer
from src.storage.chat_store import (
    add_message,
    auto_name_session,
    create_session,
    delete_session,
    load_sessions,
)
from src.ui.artifacts_panel import (
    generate_and_display_artifact,
    is_panel_open,
    render_artifact_panel,
)

# ---------------------------------------------------------------------------
# Inline style constants (Streamlit strips class attributes)
# ---------------------------------------------------------------------------

_USER_MSG = (
    "background:#ffffff; border-left:4px solid #d97706; border-radius:12px; "
    "padding:14px 18px; margin:12px 0 12px 48px; max-width:78%; float:right; clear:both; "
    "box-shadow:0 1px 2px rgba(0,0,0,0.04); font-size:0.9375rem; line-height:1.6; color:#1c1b1a;"
)

_ASSISTANT_MSG = (
    "background:#ffffff; border-radius:12px; padding:16px 20px; margin:12px 0; "
    "box-shadow:0 1px 2px rgba(0,0,0,0.04); border:1px solid #e7e5e2; "
    "font-size:0.9375rem; line-height:1.6; color:#1c1b1a; position:relative; clear:both;"
)

_CITATION_PILL = (
    "display:inline-block; background:#d97706; color:white; font-size:0.7rem; "
    "font-weight:600; padding:1px 6px; border-radius:10px; cursor:pointer; "
    "margin:0 2px; vertical-align:super;"
)

_SOURCE_CHUNK = (
    "background:#faf9f7; border-left:3px solid #d97706; border-radius:0 8px 8px 0; "
    "padding:10px 14px; margin:8px 0; font-size:0.82rem; color:#1c1b1a;"
)

_SOURCE_LABEL = "font-weight:600; color:#d97706; font-size:0.78rem; margin-bottom:4px;"

_COPY_BTN = (
    "background:none; border:1px solid #e7e5e2; border-radius:6px; padding:2px 8px; "
    "font-size:0.75rem; color:#78716c; cursor:pointer; float:right;"
)


# ---------------------------------------------------------------------------
# Top bar
# ---------------------------------------------------------------------------


def render_top_bar() -> None:
    """Render the top bar with subject name, session name, and Clear Chat."""
    subject = st.session_state.get("current_subject", "")
    session_id = st.session_state.get("current_session_id")

    session_name = ""
    if session_id and subject:
        sessions = load_sessions(subject)
        if session_id in sessions:
            session_name = sessions[session_id].name

    cols = st.columns([4, 1])
    with cols[0]:
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:8px;padding:4px 0;">'
            f'<span style="font-size:1rem;font-weight:600;color:#1c1b1a;">{subject}</span>'
            f'<span style="color:#a8a29e;font-size:1.2rem;font-weight:300;">·</span>'
            f'<span style="font-size:0.85rem;color:#78716c;overflow:hidden;'
            f'text-overflow:ellipsis;white-space:nowrap;">{session_name}</span>'
            f"</div>",
            unsafe_allow_html=True,
        )
    with cols[1]:
        if st.button(
            "🗑 Clear",
            key="clear_chat",
            help="Clear current chat session",
            use_container_width=True,
        ):
            if session_id and subject:
                delete_session(subject, session_id)
                new_id = create_session(subject)
                st.session_state.current_session_id = new_id
                st.rerun()


# ---------------------------------------------------------------------------
# Message rendering
# ---------------------------------------------------------------------------


def _render_citations(sources: list[SourceChunk]) -> str:
    """Render clickable citation pills."""
    if not sources:
        return ""
    pills = []
    for i, src in enumerate(sources, 1):
        pills.append(
            f'<span style="{_CITATION_PILL}" '
            f'onclick="this.nextElementSibling.style.display='
            f"this.nextElementSibling.style.display==='none'?'block':'none'\">"
            f"[{i}]</span>"
            f'<div style="{_SOURCE_CHUNK} display:none;">'
            f'<div style="{_SOURCE_LABEL}">{src.label}</div>'
            f"{src.content}</div>"
        )
    return " ".join(pills)


def _render_source_chunks(sources: list[SourceChunk]) -> str:
    """Render expandable source chunks."""
    if not sources:
        return ""
    html = '<div style="margin-top:8px;">'
    html += '<details><summary style="color:#d97706;cursor:pointer;font-size:0.82rem;">View sources</summary>'
    for i, src in enumerate(sources, 1):
        html += (
            f'<div style="{_SOURCE_CHUNK}">'
            f'<div style="{_SOURCE_LABEL}">[{i}] {src.label}</div>'
            f"{src.content}</div>"
        )
    html += "</details></div>"
    return html


def _get_copy_button_html(text: str) -> str:
    """Generate a copy button with JavaScript copy functionality."""
    escaped = text.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
    return (
        f'<button style="{_COPY_BTN}" onclick="navigator.clipboard.writeText(`{escaped}`);'
        f'this.innerHTML=\'Copied!\'; setTimeout(()=>this.innerHTML=\'Copy\',1500)">'
        f"Copy</button>"
    )


def render_message(msg: ChatMessage, idx: int) -> None:
    """Render a single chat message."""
    if msg.role == "user":
        st.markdown(
            f'<div style="{_USER_MSG}">{msg.content}</div>',
            unsafe_allow_html=True,
        )
    else:
        copy_html = _get_copy_button_html(msg.content)
        citations_html = _render_citations(msg.sources)
        sources_html = _render_source_chunks(msg.sources)

        st.markdown(
            f'<div style="{_ASSISTANT_MSG}">'
            f'<div style="white-space:pre-wrap;word-wrap:break-word;">{msg.content}</div>'
            f'<div style="margin-top:8px;">{copy_html}</div>'
            f'<div style="margin-top:8px;">{citations_html}</div>'
            f"{sources_html}"
            f"</div>",
            unsafe_allow_html=True,
        )


def render_messages() -> None:
    """Render all messages in the current session."""
    subject = st.session_state.get("current_subject")
    session_id = st.session_state.get("current_session_id")

    if not subject or not session_id:
        return

    sessions = load_sessions(subject)
    if session_id not in sessions:
        return

    session = sessions[session_id]
    if not session.messages:
        _render_suggested_questions()
        return

    for idx, msg in enumerate(session.messages):
        render_message(msg, idx)


# ---------------------------------------------------------------------------
# Suggested questions
# ---------------------------------------------------------------------------


def _render_suggested_questions() -> None:
    """Render suggested questions for empty sessions."""
    questions = [
        "What are the main topics covered in this subject?",
        "Can you summarize the key concepts?",
        "What are the most important formulas or definitions?",
    ]
    st.markdown(
        '<div style="text-align:center;margin-top:48px;margin-bottom:24px;">'
        '<div style="font-size:0.85rem;color:#78716c;font-weight:500;margin-bottom:16px;">'
        "Suggested questions</div></div>",
        unsafe_allow_html=True,
    )
    for i, q in enumerate(questions):
        if st.button(
            q,
            key=f"sugg_q_{i}",
            use_container_width=True,
        ):
            st.session_state.pending_question = q
            st.rerun()


# ---------------------------------------------------------------------------
# Streaming response
# ---------------------------------------------------------------------------


def _handle_user_input() -> None:
    """Handle user input and generate streaming response."""
    subject = st.session_state.get("current_subject")
    session_id = st.session_state.get("current_session_id")

    if not subject or not session_id:
        return

    prompt = st.chat_input(
        placeholder=f"Ask about {subject}..." if subject else "Ask a question..."
    )

    # Check for a pending question from suggested questions
    if not prompt and st.session_state.get("pending_question"):
        prompt = st.session_state.pending_question
        st.session_state.pending_question = None

    if not prompt:
        return

    # Check for slash commands (artifact generation)
    if prompt.startswith("/"):
        _handle_slash_command(prompt, subject, session_id)
        return

    # Save user message
    add_message(subject, session_id, "user", prompt)
    auto_name_session(subject, session_id, prompt)

    # Get settings from session state
    top_k = st.session_state.get("top_k", 4)
    max_history = st.session_state.get("max_history", 5)
    temperature = st.session_state.get("temperature", 0.3)
    search_all = st.session_state.get("search_all", False)

    # Load chat history for context
    sessions = load_sessions(subject)
    chat_history = sessions[session_id].messages if session_id in sessions else []

    # Stream response
    with st.spinner("Thinking..."):
        full_response = ""
        sources = []
        try:
            for token, chunks in get_answer(
                question=prompt,
                subject=subject,
                chat_history=chat_history,
                top_k=top_k,
                max_history=max_history,
                temperature=temperature,
                search_all_subjects=search_all,
            ):
                if chunks:
                    sources = chunks
                full_response += token
        except Exception as e:
            full_response = f"Error: {str(e)}"

    # Save assistant message
    add_message(subject, session_id, "assistant", full_response, sources)
    st.rerun()


# ---------------------------------------------------------------------------
# Slash commands
# ---------------------------------------------------------------------------


def _handle_slash_command(prompt: str, subject: str, session_id: str) -> None:
    """Handle slash commands for artifact generation."""
    command, args = parse_slash_command(prompt)

    if command is None:
        add_message(subject, session_id, "user", prompt)
        add_message(
            subject,
            session_id,
            "assistant",
            f"Unknown command: {prompt}. Available commands: /summary, /glossary, /compare, /explain",
        )
        st.rerun()
        return

    # Save the command as a user message
    add_message(subject, session_id, "user", prompt)

    # Validate arguments
    if command in ("summary", "glossary") and not args:
        add_message(
            subject,
            session_id,
            "assistant",
            f"Please specify a filename. Example: /{command} filename.pdf",
        )
        st.rerun()
        return

    if command in ("compare", "explain") and not args:
        add_message(
            subject,
            session_id,
            "assistant",
            f"Please specify a topic. Example: /{command} <topic>",
        )
        st.rerun()
        return

    # Generate artifact and display in panel
    topic = args if command in ("compare", "explain") else ""
    source_file = args if command in ("summary", "glossary") else ""

    generate_and_display_artifact(
        artifact_type=command,
        source_file=source_file,
        subject=subject,
        topic=topic,
        temperature=st.session_state.get("temperature", 0.3),
    )

    # Save assistant confirmation message
    artifact_name = f"{command.capitalize()}: {source_file or topic}"
    add_message(subject, session_id, "assistant", f"Generated: {artifact_name}")
    st.rerun()


# ---------------------------------------------------------------------------
# Main chat render
# ---------------------------------------------------------------------------


def render_chat() -> None:
    """Render the complete chat interface with optional artifact panel."""
    if is_panel_open():
        chat_col, panel_col = st.columns([3, 1])
        with chat_col:
            render_top_bar()
            render_messages()
            _handle_user_input()
        with panel_col:
            render_artifact_panel()
    else:
        # Center the chat content with side padding columns
        left_pad, center, right_pad = st.columns([1, 6, 1])
        with center:
            render_top_bar()
            render_messages()
            _handle_user_input()
