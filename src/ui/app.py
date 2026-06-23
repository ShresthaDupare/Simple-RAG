"""Main Streamlit app — page config, session state, routing."""

import sys
from pathlib import Path

# Ensure src/ is on the path
_root = Path(__file__).resolve().parent.parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

import streamlit as st

from src.config import (
    DEFAULT_CHUNK_OVERLAP,
    DEFAULT_CHUNK_SIZE,
    DEFAULT_MAX_HISTORY,
    DEFAULT_TEMPERATURE,
    DEFAULT_TOP_K,
)
from src.loaders.scanner import scan_subjects
from src.storage.chat_store import load_sessions
from src.ui.styles import GLOBAL_CSS

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Study RAG",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject global CSS
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Session state defaults
# ---------------------------------------------------------------------------

_defaults: dict[str, object] = {
    # Current subject & session
    "current_subject": None,
    "current_session_id": None,
    # Subject list (refreshed on startup)
    "subjects": [],
    # Settings
    "top_k": DEFAULT_TOP_K,
    "max_history": DEFAULT_MAX_HISTORY,
    "temperature": DEFAULT_TEMPERATURE,
    "chunk_size": DEFAULT_CHUNK_SIZE,
    "chunk_overlap": DEFAULT_CHUNK_OVERLAP,
    # Search
    "search_all": False,
    # Artifact panel
    "artifact_panel_open": False,
    "current_artifact": None,
}

for key, value in _defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------------------------------------------------------------------
# Refresh subjects on startup
# ---------------------------------------------------------------------------

st.session_state.subjects = scan_subjects()

# Auto-select first subject if none selected and subjects exist
if st.session_state.current_subject is None and st.session_state.subjects:
    st.session_state.current_subject = st.session_state.subjects[0]


# ---------------------------------------------------------------------------
# Helper: get current sessions dict
# ---------------------------------------------------------------------------

def _get_sessions() -> dict:
    """Load sessions for the current subject."""
    if not st.session_state.current_subject:
        return {}
    return load_sessions(st.session_state.current_subject)


# Expose to other modules
st.session_state["_get_sessions"] = _get_sessions

# ---------------------------------------------------------------------------
# Main layout
# ---------------------------------------------------------------------------

from src.ui.sidebar import render_sidebar  # noqa: E402

render_sidebar()

# Main chat area placeholder — will be built in Phase 8
main = st.container()

with main:
    if not st.session_state.subjects:
        st.markdown(
            "<div style='text-align:center; margin-top:80px; color:#888;'>"
            "<h2>📚 Study RAG</h2>"
            "<p>No subjects found. Create folders in <code>data/</code> and add PDF or PPTX files.</p>"
            "</div>",
            unsafe_allow_html=True,
        )
    elif not st.session_state.current_session_id:
        st.markdown(
            "<div style='text-align:center; margin-top:80px; color:#888;'>"
            "<p>Select a chat from the sidebar, or start a new one.</p>"
            "</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<div style='text-align:center; margin-top:80px; color:#888;'>"
            "<p>Chat UI will be built in Phase 8.</p>"
            "</div>",
            unsafe_allow_html=True,
        )
