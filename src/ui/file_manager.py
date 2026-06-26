"""File Manager UI — upload, list, delete files, and rebuild index."""

import shutil
from pathlib import Path

import streamlit as st

from src.config import DATA_DIR, FAISS_DIR, SUPPORTED_EXTENSIONS
from src.exceptions import IndexNotFoundError
from src.loaders.scanner import get_files, scan_subjects
from src.retrieval.vector_store import create_index, delete_index, index_exists


# ---------------------------------------------------------------------------
# File Manager entry point
# ---------------------------------------------------------------------------


def render_file_manager() -> None:
    """Render the file manager section in the sidebar or main area."""
    subject = st.session_state.get("current_subject")
    if not subject:
        st.info("Select a subject first.")
        return

    # Back button to return to chat
    if st.button("← Back to Chat", use_container_width=True, key="back_to_chat"):
        st.session_state["show_file_manager"] = False
        st.rerun()

    st.subheader(f"📁 Files — {subject}")

    # Upload button
    if st.button("⬆️ Upload Files", use_container_width=True, key="upload_btn"):
        st.session_state["show_upload_modal"] = True
        st.rerun()

    # Render upload modal if triggered
    if st.session_state.get("show_upload_modal"):
        _render_upload_modal(subject)

    # File list
    _render_file_list(subject)

    # Rebuild index
    st.markdown("---")
    _render_rebuild_section(subject)


# ---------------------------------------------------------------------------
# Upload modal
# ---------------------------------------------------------------------------


def _render_upload_modal(subject: str) -> None:
    """Render a file upload dialog using st.dialog (Streamlit ≥ 1.37)."""
    @st.dialog("Upload Files", width="large")
    def _upload_dialog():
        subject_dir = DATA_DIR / subject
        subject_dir.mkdir(parents=True, exist_ok=True)

        allowed = ", ".join(f"*{ext}" for ext in sorted(SUPPORTED_EXTENSIONS))
        st.markdown(
            '<div style="border:2px dashed #e7e5e2;border-radius:12px;padding:24px;text-align:center;">',
            unsafe_allow_html=True,
        )
        uploaded = st.file_uploader(
            f"Choose files ({allowed})",
            type=list(SUPPORTED_EXTENSIONS),
            accept_multiple_files=True,
            key="file_uploader",
        )
        st.markdown("</div>", unsafe_allow_html=True)

        if uploaded:
            st.markdown(f"**{len(uploaded)} file(s) selected**")
            for f in uploaded:
                st.caption(f"• {f.name} ({f.size / 1024:.1f} KB)")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Upload", type="primary", use_container_width=True, disabled=not uploaded):
                for f in uploaded:
                    dest = subject_dir / f.name
                    with open(dest, "wb") as out:
                        out.write(f.getbuffer())
                st.success(f"Uploaded {len(uploaded)} file(s) to {subject}/")
                st.session_state["show_upload_modal"] = False
                st.rerun()
        with c2:
            if st.button("Cancel", use_container_width=True):
                st.session_state["show_upload_modal"] = False
                st.rerun()

    _upload_dialog()


# ---------------------------------------------------------------------------
# File list with delete
# ---------------------------------------------------------------------------


def _render_file_list(subject: str) -> None:
    """List all files in the subject folder with delete buttons."""
    try:
        files = get_files(subject)
    except Exception:
        files = []

    if not files:
        st.caption("No files in this subject yet.")
        return

    st.markdown(f"**{len(files)} file(s)**")

    for file_path in files:
        icon = "📄" if file_path.suffix == ".pdf" else "📊"
        size_kb = file_path.stat().st_size / 1024
        has_index = index_exists(subject)

        status_color = "#059669" if has_index else "#d97706"
        status_bg = "#ecfdf5" if has_index else "#fffbeb"
        status_label = "Indexed" if has_index else "Not indexed"

        cols = st.columns([6, 1])
        with cols[0]:
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:8px;padding:8px 0;">'
                f'<span>{icon}</span>'
                f'<span style="flex:1;font-size:0.9rem;color:#1c1b1a;overflow:hidden;'
                f'text-overflow:ellipsis;white-space:nowrap;">{file_path.name}</span>'
                f'<span style="font-size:0.75rem;color:#78716c;">{size_kb:.0f} KB</span>'
                f'<span style="font-size:0.7rem;padding:2px 8px;border-radius:10px;'
                f'background:{status_bg};color:{status_color};">{status_label}</span>'
                f"</div>",
                unsafe_allow_html=True,
            )
        with cols[1]:
            if st.button("🗑️", key=f"del_{file_path.name}", help="Delete file"):
                file_path.unlink()
                if index_exists(subject):
                    delete_index(subject)
                st.rerun()


# ---------------------------------------------------------------------------
# Rebuild index section
# ---------------------------------------------------------------------------


def _render_rebuild_section(subject: str) -> None:
    """Render rebuild index button with progress indication."""
    has_index = index_exists(subject)

    if has_index:
        st.markdown("✅ Index exists")
        if st.button("🔄 Rebuild Index", use_container_width=True, key="rebuild_btn"):
            _rebuild_index(subject)
    else:
        st.markdown("⚠️ No index for this subject")
        if st.button("🔨 Build Index", use_container_width=True, type="primary", key="build_btn"):
            _rebuild_index(subject)


def _rebuild_index(subject: str) -> None:
    """Build or rebuild the FAISS index with a progress bar."""
    from src.loaders import load_and_chunk

    files = get_files(subject)
    if not files:
        st.warning("No files to index. Upload files first.")
        return

    progress_bar = st.progress(0, text="Loading documents...")
    status_text = st.empty()

    try:
        # Step 1: Load and chunk
        status_text.text("Loading and chunking documents...")
        progress_bar.progress(20, text="Loading documents...")
        chunks = load_and_chunk(subject)

        if not chunks:
            st.warning("No chunks extracted. Check your files.")
            progress_bar.empty()
            status_text.empty()
            return

        # Step 2: Build index
        status_text.text(f"Building index for {len(chunks)} chunks...")
        progress_bar.progress(60, text="Building vector index...")

        # Delete old index if exists
        if index_exists(subject):
            delete_index(subject)

        num_vectors = create_index(subject, chunks)

        # Done
        progress_bar.progress(100, text="Done!")
        status_text.text(f"✅ Index built: {num_vectors} vectors from {len(files)} file(s)")
        st.rerun()

    except Exception as e:
        st.error(f"Failed to build index: {e}")
        progress_bar.empty()
        status_text.empty()
