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
from src.ui.artifacts_panel import render_artifact_list_sidebar


# ---------------------------------------------------------------------------
# Sidebar entry point
# ---------------------------------------------------------------------------


def render_sidebar() -> None:
    """Render the full sidebar: title, search, subjects, sessions, settings."""
    with st.sidebar:
        st.markdown(
            '<div style="display:flex;align-items:center;gap:8px;padding:4px 0 0 0;">'
            '<span style="font-size:1.4rem;">📚</span>'
            '<span style="font-size:1.25rem;font-weight:700;color:#f0ebe5;'
            'letter-spacing:-0.02em;">Study RAG</span>'
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p style="font-size:0.75rem;color:var(--sidebar-text-dim);'
            "margin:-4px 0 12px 0;\">"
            "Study assistant with RAG</p>",
            unsafe_allow_html=True,
        )

        # -- Search bar --------------------------------------------------------
        search_query = st.text_input(
            "Search sessions",
            placeholder="Search sessions...",
            label_visibility="collapsed",
            key="sidebar_search",
        )

        # -- New Chat button ---------------------------------------------------
        if st.button("+ New Chat", use_container_width=True, type="primary"):
            _handle_new_chat()

        st.markdown("---")

        # -- Subject groups ----------------------------------------------------
        subjects = st.session_state.get("subjects", [])
        if subjects:
            _render_subjects(subjects, search_query)
        else:
            st.markdown(
                '<div style="background-color:#262320; border-left:3px solid #d97706; '
                "padding:10px 12px; border-radius:6px; margin-top:8px; "
                "color:#d4cfc8; font-size:0.85rem;\">"
                "📁 No subjects found in <code>data/</code>.<br>"
                '<span style="font-size:0.78rem; color:#9d9690;">'
                "Create a folder and add PDF/PPTX files.</span></div>",
                unsafe_allow_html=True,
            )

        # -- File Manager button -----------------------------------------------
        st.markdown("---")
        if st.button("📂 Manage Files", use_container_width=True, key="manage_files_btn"):
            st.session_state["show_file_manager"] = True
            st.rerun()

        # -- Artifact list (per subject) ---------------------------------------
        current_subject = st.session_state.get("current_subject")
        if current_subject:
            render_artifact_list_sidebar(current_subject)

        # -- Settings (bottom) -------------------------------------------------
        st.markdown("---")
        _render_settings()


# ---------------------------------------------------------------------------
# New chat
# ---------------------------------------------------------------------------


def _handle_new_chat(subject_override: str | None = None) -> None:
    """Create a new chat session for the current subject."""
    subject = subject_override or st.session_state.get("current_subject")
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
    """Render collapsible subject groups with session lists and color dots."""
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

        # Subject header with color dot shown inside the expander when opened.
        # (Streamlit expanders cannot be wrapped in custom HTML divs,
        #  so the dot is rendered as a meta row inside the expander body.)
        with st.expander(
            f"**{subject}**",
            expanded=is_active_subject,
        ):
            # Subject meta row with color dot + session count
            st.markdown(
                f'<div class="subject-meta-row">'
                f'<span class="subject-dot-render" '
                f'style="display:inline-block;width:10px;height:10px;'
                f"border-radius:50%;background:{color};flex-shrink:0;\"></span>"
                f'<span class="subject-session-count">'
                f"{len(sessions)} chat(s)</span></div>",
                unsafe_allow_html=True,
            )

            # + New Chat button per subject
            if st.button(
                "+ New Chat",
                key=f"new_chat_{subject}",
                use_container_width=True,
            ):
                _handle_new_chat(subject_override=subject)

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
        btn_type = "primary" if is_active else "secondary"
        if st.button(
            label,
            key=f"session_{session_id}",
            use_container_width=True,
            type=btn_type,
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
        # Search All toggle
        st.markdown(
            '<div class="search-all-wrapper">',
            unsafe_allow_html=True,
        )
        st.session_state.search_all = st.checkbox(
            "Search all subjects",
            value=st.session_state.search_all,
            key="search_all_checkbox",
            help="When checked, queries search across all subjects simultaneously",
        )
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("---")

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
