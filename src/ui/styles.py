"""All CSS for the Streamlit app — sidebar, messages, input, responsive."""

GLOBAL_CSS = """
<style>
/* -------------------------------------------------------------------------
   Root variables
   ------------------------------------------------------------------------- */
:root {
    --bg: #ffffff;
    --sidebar-bg: #1a1a2e;
    --sidebar-text: #e0e0e0;
    --sidebar-hover: #2a2a4a;
    --sidebar-active: #3a3a5a;
    --primary: #6366f1;
    --primary-light: #f0f0ff;
    --user-msg-bg: #f0f0ff;
    --input-bg: #f7f7f8;
    --input-border: #e5e5e5;
    --text: #1a1a2e;
    --subtle: #888888;
}

/* -------------------------------------------------------------------------
   Global
   ------------------------------------------------------------------------- */
.stApp {
    background-color: var(--bg);
}

/* -------------------------------------------------------------------------
   Sidebar overrides — Streamlit 1.58.0 compatible
   ------------------------------------------------------------------------- */
section[data-testid="stSidebar"] {
    background-color: var(--sidebar-bg) !important;
}

/* All text in sidebar */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] h4,
section[data-testid="stSidebar"] h5,
section[data-testid="stSidebar"] h6,
section[data-testid="stSidebar"] li,
section[data-testid="stSidebar"] code,
section[data-testid="stSidebar"] summary,
section[data-testid="stSidebar"] [data-testid="stCaption"],
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
    color: var(--sidebar-text) !important;
}

/* Headings slightly brighter */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2 {
    color: #ffffff !important;
}

/* Text input fields */
section[data-testid="stSidebar"] .stTextInput [data-testid="stTextInputRootElement"] input {
    background-color: var(--sidebar-hover);
    color: var(--sidebar-text);
    border: 1px solid transparent;
    border-radius: 8px;
}

section[data-testid="stSidebar"] .stTextInput [data-testid="stTextInputRootElement"] input:focus {
    border-color: var(--primary);
}

section[data-testid="stSidebar"] .stTextInput [data-testid="stWidgetLabel"] {
    color: var(--sidebar-text) !important;
}

/* All buttons */
section[data-testid="stSidebar"] .stButton button {
    border-radius: 8px;
    width: 100%;
}

/* Primary buttons */
section[data-testid="stSidebar"] .stButton button[kind="primary"] {
    background-color: var(--sidebar-active);
    color: #ffffff !important;
    border: none;
}

section[data-testid="stSidebar"] .stButton button[kind="primary"]:hover {
    background-color: #5558e6;
}

section[data-testid="stSidebar"] .stButton button[kind="primary"] span {
    color: #ffffff !important;
}

/* Secondary buttons */
section[data-testid="stSidebar"] .stButton button[kind="secondary"] {
    background-color: transparent;
    color: var(--sidebar-text) !important;
    border: 1px solid transparent;
    text-align: left;
}

section[data-testid="stSidebar"] .stButton button[kind="secondary"]:hover {
    background-color: var(--sidebar-hover);
    border-color: transparent;
}

section[data-testid="stSidebar"] .stButton button[kind="secondary"] span {
    color: var(--sidebar-text) !important;
}

/* Expanders */
section[data-testid="stSidebar"] [data-testid="stExpander"] details {
    border-color: var(--sidebar-hover) !important;
}

section[data-testid="stSidebar"] [data-testid="stExpander"] summary {
    color: var(--sidebar-text) !important;
    background-color: transparent !important;
    font-weight: 600;
}

section[data-testid="stSidebar"] [data-testid="stExpander"] summary:hover {
    background-color: var(--sidebar-hover) !important;
}

section[data-testid="stSidebar"] [data-testid="stExpanderDetails"] {
    background-color: transparent !important;
    border-top-color: var(--sidebar-hover) !important;
}

section[data-testid="stSidebar"] [data-testid="stExpanderDetails"] p,
section[data-testid="stSidebar"] [data-testid="stExpanderDetails"] span,
section[data-testid="stSidebar"] [data-testid="stExpanderDetails"] label,
section[data-testid="stSidebar"] [data-testid="stExpanderDetails"] [data-testid="stWidgetLabel"] {
    color: var(--sidebar-text) !important;
}

/* Alert/info boxes */
section[data-testid="stSidebar"] [data-testid="stAlert"] {
    background-color: var(--sidebar-hover) !important;
}

section[data-testid="stSidebar"] [data-testid="stAlertContainer"] {
    background-color: var(--sidebar-hover) !important;
    border-left-color: var(--primary) !important;
}

section[data-testid="stSidebar"] [data-testid="stAlert"] p,
section[data-testid="stSidebar"] [data-testid="stAlert"] span,
section[data-testid="stSidebar"] [data-testid="stAlert"] div,
section[data-testid="stSidebar"] [data-testid="stAlert"] a,
section[data-testid="stSidebar"] [data-testid="stAlertContainer"] p,
section[data-testid="stSidebar"] [data-testid="stAlertContainer"] span {
    color: var(--sidebar-text) !important;
}

/* Slider labels and values */
section[data-testid="stSidebar"] .stSlider [data-testid="stWidgetLabel"] {
    color: var(--sidebar-text) !important;
    font-size: 0.8rem;
}

section[data-testid="stSidebar"] .stSlider [data-testid="stSliderTickBar"] {
    color: var(--sidebar-text) !important;
}

section[data-testid="stSidebar"] .stSlider [data-testid="stSliderThumbValue"] {
    color: var(--sidebar-text) !important;
}

/* Dividers */
section[data-testid="stSidebar"] hr {
    border-color: var(--sidebar-hover) !important;
    opacity: 0.5;
}

section[data-testid="stSidebar"] [data-testid="stMarkdown"] hr {
    border-color: var(--sidebar-hover) !important;
}

/* Markdown content in sidebar */
section[data-testid="stSidebar"] [data-testid="stMarkdown"] p,
section[data-testid="stSidebar"] [data-testid="stMarkdown"] span,
section[data-testid="stSidebar"] [data-testid="stMarkdown"] li,
section[data-testid="stSidebar"] [data-testid="stMarkdown"] a,
section[data-testid="stSidebar"] [data-testid="stMarkdown"] code {
    color: var(--sidebar-text) !important;
}

section[data-testid="stSidebar"] [data-testid="stMarkdown"] a {
    color: #8b8bff !important;
}

section[data-testid="stSidebar"] [data-testid="stMarkdown"] a:hover {
    color: #aaaaff !important;
}

/* -------------------------------------------------------------------------
   Sidebar subject group headers
   ------------------------------------------------------------------------- */
.subject-header {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 8px;
    margin-top: 12px;
    cursor: pointer;
    border-radius: 6px;
}

.subject-header:hover {
    background-color: var(--sidebar-hover);
}

.subject-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}

.subject-name {
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--sidebar-text);
    flex: 1;
}

/* -------------------------------------------------------------------------
   Sidebar session items
   ------------------------------------------------------------------------- */
.session-item {
    display: flex;
    align-items: center;
    padding: 6px 8px 6px 28px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.82rem;
    color: var(--sidebar-text);
    gap: 6px;
}

.session-item:hover {
    background-color: var(--sidebar-hover);
}

.session-item.active {
    background-color: var(--sidebar-active);
    font-weight: 500;
}

.session-item .session-name {
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.session-actions {
    display: none;
    gap: 4px;
}

.session-item:hover .session-actions {
    display: flex;
}

.session-actions button {
    background: none;
    border: none;
    color: var(--sidebar-text);
    cursor: pointer;
    padding: 2px 4px;
    font-size: 0.75rem;
    border-radius: 4px;
}

.session-actions button:hover {
    background-color: var(--sidebar-hover);
}

/* -------------------------------------------------------------------------
   Chat messages
   ------------------------------------------------------------------------- */
.chat-container {
    max-width: 750px;
    margin: 0 auto;
    padding: 16px 0;
}

.user-message {
    background-color: var(--user-msg-bg);
    border-radius: 12px;
    padding: 12px 16px;
    margin: 8px 0 8px 60px;
    max-width: 85%;
    font-size: 0.95rem;
    line-height: 1.5;
    color: var(--text);
}

.assistant-message {
    padding: 12px 0;
    margin: 8px 0;
    font-size: 0.95rem;
    line-height: 1.6;
    color: var(--text);
}

/* -------------------------------------------------------------------------
   Citation pills
   ------------------------------------------------------------------------- */
.citation-pill {
    display: inline-block;
    background-color: var(--primary);
    color: white;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 1px 6px;
    border-radius: 10px;
    cursor: pointer;
    margin: 0 2px;
    vertical-align: super;
}

.citation-pill:hover {
    background-color: #5558e6;
}

/* -------------------------------------------------------------------------
   Source chunks (expandable)
   ------------------------------------------------------------------------- */
.source-chunk {
    background-color: #f9f9fb;
    border-left: 3px solid var(--primary);
    border-radius: 0 8px 8px 0;
    padding: 10px 14px;
    margin: 8px 0;
    font-size: 0.82rem;
    color: var(--text);
}

.source-chunk .source-label {
    font-weight: 600;
    color: var(--primary);
    font-size: 0.78rem;
    margin-bottom: 4px;
}

/* -------------------------------------------------------------------------
   Input bar
   ------------------------------------------------------------------------- */
.stChatInput {
    border-radius: 12px;
}

div[data-testid="stChatInput"] {
    border-radius: 12px;
    background-color: var(--input-bg);
    border: 1px solid var(--input-border);
}

div[data-testid="stChatInput"] textarea {
    font-size: 0.95rem;
}

/* -------------------------------------------------------------------------
   Top bar
   ------------------------------------------------------------------------- */
.top-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 16px;
    border-bottom: 1px solid var(--input-border);
    background-color: var(--bg);
    position: sticky;
    top: 0;
    z-index: 10;
}

.top-bar-title {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text);
}

/* -------------------------------------------------------------------------
   Settings sliders
   ------------------------------------------------------------------------- */
section[data-testid="stSidebar"] .stSlider label {
    color: var(--sidebar-text) !important;
    font-size: 0.8rem;
}

/* -------------------------------------------------------------------------
   Responsive
   ------------------------------------------------------------------------- */
@media (max-width: 768px) {
    .user-message {
        margin-left: 20px;
        max-width: 90%;
    }

    .chat-container {
        padding: 8px 12px;
    }
}

/* -------------------------------------------------------------------------
   Artifact panel (placeholder for Phase 10)
   ------------------------------------------------------------------------- */
.artifact-panel {
    background-color: #fafafa;
    border-left: 1px solid var(--input-border);
    padding: 16px;
    height: 100vh;
    overflow-y: auto;
}

/* -------------------------------------------------------------------------
   Suggested questions
   ------------------------------------------------------------------------- */
.suggested-question {
    background-color: var(--primary-light);
    border: 1px solid var(--primary);
    border-radius: 8px;
    padding: 8px 14px;
    cursor: pointer;
    font-size: 0.85rem;
    color: var(--primary);
    margin: 4px 0;
    transition: background-color 0.15s;
}

.suggested-question:hover {
    background-color: #e0e0ff;
}
</style>
"""
