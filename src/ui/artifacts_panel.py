"""Artifact panel — slide-in panel, streaming, copy, download, autocomplete."""

import streamlit as st

from src.artifacts.generator import generate_artifact
from src.artifacts.parser import (
    get_available_commands,
    get_available_files,
    match_files,
    parse_slash_command,
)
from src.config import DEFAULT_TEMPERATURE
from src.models import Artifact
from src.storage.artifact_store import delete_artifact, list_artifacts, load_artifact


# ---------------------------------------------------------------------------
# Panel state helpers
# ---------------------------------------------------------------------------


def open_artifact_panel(artifact: Artifact | None = None) -> None:
    """Open the artifact panel, optionally showing a specific artifact."""
    st.session_state["artifact_panel_open"] = True
    if artifact:
        st.session_state["current_artifact"] = artifact


def close_artifact_panel() -> None:
    """Close the artifact panel."""
    st.session_state["artifact_panel_open"] = False
    st.session_state["current_artifact"] = None


def is_panel_open() -> bool:
    """Check if the artifact panel is currently open."""
    return st.session_state.get("artifact_panel_open", False)


# ---------------------------------------------------------------------------
# Autocomplete for slash commands
# ---------------------------------------------------------------------------


def render_autocomplete(text_input: str, subject: str) -> str | None:
    """Show autocomplete suggestions for slash commands.

    Returns the completed command if user selects one, else None.
    """
    if not text_input.startswith("/"):
        return None

    parts = text_input.split(maxsplit=1)
    command_part = parts[0]
    args_part = parts[1] if len(parts) > 1 else ""

    commands = get_available_commands()

    # If user is still typing the command, show command suggestions
    if len(command_part) <= 10 and not args_part:
        matching = [
            c for c in commands if c["command"].startswith(command_part)
        ]
        if matching:
            with st.popover("Commands", use_container_width=True):
                for cmd in matching:
                    if st.button(
                        f"`{cmd['command']}` — {cmd['description']}",
                        key=f"ac_{cmd['command']}",
                        use_container_width=True,
                    ):
                        return cmd["command"] + " "
        return None

    # If command is complete, show file suggestions for summary/glossary
    command_name = command_part.lstrip("/")
    if command_name in ("summary", "glossary") and args_part:
        files = get_available_files(subject)
        matching = match_files(args_part, files)
        if matching:
            with st.popover("Files", use_container_width=True):
                for fname in matching:
                    if st.button(
                        fname,
                        key=f"file_ac_{fname}",
                        use_container_width=True,
                    ):
                        return command_part + " " + fname
    return None


# ---------------------------------------------------------------------------
# Artifact panel (right side)
# ---------------------------------------------------------------------------


def render_artifact_panel() -> None:
    """Render the artifact slide-in panel on the right side."""
    if not is_panel_open():
        return

    artifact = st.session_state.get("current_artifact")

    with st.container():
        st.markdown(
            '<div class="artifact-panel">',
            unsafe_allow_html=True,
        )

        # Panel header with close button
        header_cols = st.columns([5, 1])
        with header_cols[0]:
            if artifact:
                st.markdown(f"<h3>{artifact.name}</h3>", unsafe_allow_html=True)
            else:
                st.markdown("<h3>Artifact</h3>", unsafe_allow_html=True)
        with header_cols[1]:
            if st.button("✕", key="close_artifact_panel", help="Close"):
                close_artifact_panel()
                st.rerun()

        st.markdown("---")

        if artifact:
            _render_artifact_content(artifact)
        else:
            st.info("No artifact selected.")

        st.markdown("</div>", unsafe_allow_html=True)


def _render_artifact_content(artifact: Artifact) -> None:
    """Render the content of an artifact with copy/download buttons."""
    # Load artifact content from disk
    loaded = load_artifact(artifact.id, artifact.subject)
    if loaded is None:
        st.error("Artifact not found on disk.")
        return

    _, body = loaded

    # Action buttons
    st.markdown(
        '<div class="artifact-action-bar">',
        unsafe_allow_html=True,
    )
    _render_copy_button(body, artifact.id)
    _render_download_button(body, artifact)
    if st.button("🗑️ Delete", key=f"del_art_{artifact.id}", help="Delete artifact"):
        delete_artifact(artifact.id, artifact.subject)
        close_artifact_panel()
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # Render artifact markdown content
    st.markdown(body)


def _render_copy_button(content: str, artifact_id: str) -> None:
    """Render a copy button that copies artifact content to clipboard."""
    escaped = content.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
    js = (
        f"navigator.clipboard.writeText(`{escaped}`);"
        f"this.innerHTML='Copied!';"
        f"setTimeout(()=>this.innerHTML='📋 Copy',1500)"
    )
    st.markdown(
        f'<button onclick="{js}" class="artifact-copy-btn">📋 Copy</button>',
        unsafe_allow_html=True,
    )


def _render_download_button(content: str, artifact: Artifact) -> None:
    """Render a download button for the artifact as .md file."""
    filename = f"{artifact.type}_{artifact.id[:8]}.md"
    st.download_button(
        label="⬇️ Download",
        data=content,
        file_name=filename,
        mime="text/markdown",
        key=f"dl_art_{artifact.id}",
        help="Download as .md file",
        use_container_width=True,
    )


# ---------------------------------------------------------------------------
# Streaming artifact generation (called from chat.py)
# ---------------------------------------------------------------------------


def generate_and_display_artifact(
    artifact_type: str,
    source_file: str,
    subject: str,
    topic: str = "",
    temperature: float = DEFAULT_TEMPERATURE,
) -> None:
    """Generate an artifact with streaming display in the panel.

    This is called from chat.py when a slash command is detected.
    It opens the panel and streams the artifact content into it.
    """
    # Open the panel first
    open_artifact_panel()

    # Use st.status for streaming display
    with st.status(f"Generating {artifact_type}...", expanded=True) as status:
        full_text = ""
        artifact_meta = None
        try:
            for token, artifact in generate_artifact(
                artifact_type=artifact_type,
                source_file=source_file,
                subject=subject,
                topic=topic,
                temperature=temperature,
            ):
                if artifact_meta is None:
                    artifact_meta = artifact
                    st.session_state["current_artifact"] = artifact
                full_text += token
                # Display streaming text
                st.markdown(
                    f'<div class="artifact-content">{full_text}</div>',
                    unsafe_allow_html=True,
                )
        except Exception as e:
            status.update(label=f"Error: {e}", state="error")
            return

        status.update(label=f"✅ {artifact_type.capitalize()} generated", state="complete")

    # Final render of the complete artifact
    if full_text and artifact_meta:
        st.session_state["current_artifact"] = artifact_meta


# ---------------------------------------------------------------------------
# Artifact list in sidebar
# ---------------------------------------------------------------------------


def render_artifact_list_sidebar(subject: str) -> None:
    """Render the list of saved artifacts in the sidebar."""
    artifacts = list_artifacts(subject)
    if not artifacts:
        return

    with st.expander("📄 Saved Artifacts", expanded=False):
        for art in artifacts:
            col1, col2 = st.columns([5, 1])
            with col1:
                if st.button(
                    art.name,
                    key=f"art_sidebar_{art.id}",
                    use_container_width=True,
                    help=f"Open {art.type}",
                ):
                    open_artifact_panel(art)
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"art_del_sidebar_{art.id}", help="Delete"):
                    delete_artifact(art.id, subject)
                    st.rerun()
