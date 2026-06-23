"""Sidebar rendering — subjects, sessions, settings."""

import streamlit as st

from src.config import (
    CHUNK_OVERLAP_RANGE,
    CHUNK_SIZE_RANGE,
    MAX_HISTORY_RANGE,
    TEMPERATURE_RANGE,
    TOP_K_RANGE,
    get_subject_color,
)
from src.loaders.scanner import scan_subjects
from src.storage.chat_store import (
    create_session,
    delete_session,
    load_sessions,
    rename_session,
)


# ---------------------------------------------------------------------------
# Sidebar entry point
# ---------------------------------------------------------------------------

def render_sidebar() -> None:
    """Render the full sidebar: title, search, subjects, sessions, settings."""
    with st.sidebar:
        st.markdown("# 📚 Study RAG")
        st.markdown("")

        # -- Search bar --------------------------------------------------------
        search_query = st.text_input(
            "Search sessions",
            placeholder="Search sessions...",
            label_visibility="collapsed",
            key="sidebar_search",
        )

        # -- New Chat button ---------------------------------------------------
        if st.button("+ New Chat", use_container_width=True):
            _handle_new_chat()

        st.markdown("---")

        # -- Subject groups ----------------------------------------------------
        subjects = st.session_state.get("subjects", [])
        if subjects:
            _render_subjects(subjects, search_query)
        else:
            st.markdown(
                '<div style="background-color:#2a2a4a; border-left:3px solid #6366f1; '
                'padding:10px 12px; border-radius:6px; margin-top:8px; '
                'color:#e0e0e0; font-size:0.85rem;">'
                '📁 No subjects found in <code>data/</code>.<br>'
                '<span style="font-size:0.78rem; color:#aaa;">'
                'Create a folder and add PDF/PPTX files.</span></div>',
                unsafe_allow_html=True,
            )

        # -- Settings (bottom) -------------------------------------------------
        st.markdown("---")
        _render_settings()


# ---------------------------------------------------------------------------
# New chat
# ---------------------------------------------------------------------------

def _handle_new_chat() -> None:
    """Create a new chat session for the current subject."""
    subject = st.session_state.get("current_subject")
    if not subject:
        subjects = scan_subjects()
        if subjects:
            st.session_state.current_subject = subjects[0]
            subject = subjects[0]
        else:
            return
    sid = create_session(subject)
    st.session_state.current_session_id = sid
    st.rerun()


# ---------------------------------------------------------------------------
# Subject groups + session list
# ---------------------------------------------------------------------------

def _render_subjects(subjects: list[str], search_query: str) -> None:
    """Render collapsible subject groups with session lists."""
    for subject in subjects:
        color = get_subject_color(subject)
        sessions = load_sessions(subject)
        is_active_subject = st.session_state.current_subject == subject

        # Filter sessions by search
        if search_query:
            sessions = {
                sid: s
                for sid, s in sessions.items()
                if search_query.lower() in s.name.lower()
            }

        # Subject header
        with st.expander(
            f"**{subject}**",
            expanded=is_active_subject,
        ):
            # + New Chat button per subject
            if st.button(
                "+ New Chat",
                key=f"new_chat_{subject}",
                use_container_width=True,
            ):
                sid = create_session(subject)
                st.session_state.current_subject = subject
                st.session_state.current_session_id = sid
                st.rerun()

            # Session list
            if not sessions:
                st.caption("No chats yet")
            else:
                for sid, session in sessions.items():
                    is_active = (
                        st.session_state.current_session_id == sid
                        and is_active_subject
                    )
                    _render_session_item(
                        subject=subject,
                        session_id=sid,
                        session_name=session.name,
                        is_active=is_active,
                    )


def _render_session_item(
    subject: str,
    session_id: str,
    session_name: str,
    is_active: bool,
) -> None:
    """Render a single session row with active highlight and hover actions."""
    col1, col2, col3 = st.columns([6, 1, 1])

    with col1:
        label = f"{'▸ ' if is_active else ''}{session_name}"
        if st.button(
            label,
            key=f"session_{session_id}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
        ):
            st.session_state.current_subject = subject
            st.session_state.current_session_id = session_id
            st.rerun()

    with col2:
        if st.button("✏️", key=f"rename_{session_id}", help="Rename"):
            st.session_state[f"renaming_{session_id}"] = True
            st.rerun()

    with col3:
        if st.button("🗑️", key=f"delete_{session_id}", help="Delete"):
            delete_session(subject, session_id)
            if st.session_state.current_session_id == session_id:
                st.session_state.current_session_id = None
            st.rerun()

    # Inline rename form
    if st.session_state.get(f"renaming_{session_id}"):
        new_name = st.text_input(
            "New name",
            value=session_name,
            key=f"rename_input_{session_id}",
            label_visibility="collapsed",
        )
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Save", key=f"save_rename_{session_id}"):
                rename_session(subject, session_id, new_name)
                st.session_state[f"renaming_{session_id}"] = False
                st.rerun()
        with c2:
            if st.button("Cancel", key=f"cancel_rename_{session_id}"):
                st.session_state[f"renaming_{session_id}"] = False
                st.rerun()


# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------

def _render_settings() -> None:
    """Render settings sliders at the bottom of the sidebar."""
    with st.expander("⚙ Settings", expanded=False):
        st.session_state.top_k = st.slider(
            "Top-K results",
            min_value=TOP_K_RANGE[0],
            max_value=TOP_K_RANGE[1],
            value=st.session_state.top_k,
            key="slider_top_k",
        )
        st.session_state.max_history = st.slider(
            "Max history turns",
            min_value=MAX_HISTORY_RANGE[0],
            max_value=MAX_HISTORY_RANGE[1],
            value=st.session_state.max_history,
            key="slider_max_history",
        )
        st.session_state.temperature = st.slider(
            "Temperature",
            min_value=TEMPERATURE_RANGE[0],
            max_value=TEMPERATURE_RANGE[1],
            value=st.session_state.temperature,
            step=0.05,
            key="slider_temperature",
        )
        st.session_state.chunk_size = st.slider(
            "Chunk size",
            min_value=CHUNK_SIZE_RANGE[0],
            max_value=CHUNK_SIZE_RANGE[1],
            value=st.session_state.chunk_size,
            step=100,
            key="slider_chunk_size",
        )
        st.session_state.chunk_overlap = st.slider(
            "Chunk overlap",
            min_value=CHUNK_OVERLAP_RANGE[0],
            max_value=CHUNK_OVERLAP_RANGE[1],
            value=st.session_state.chunk_overlap,
            step=50,
            key="slider_chunk_overlap",
        )
