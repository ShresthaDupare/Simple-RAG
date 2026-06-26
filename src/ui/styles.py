"""All CSS for the Streamlit app — Design System v2 'Warm Academia'."""

# Load Inter font + Material Icons via Google Fonts
FONT_LINK = (
    '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">'
    '<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet">'
)

# ---------------------------------------------------------------------------
# BASE CSS — essential visual styles. No :has() selectors.
# If this block fails, the app has no custom styling at all.
# ---------------------------------------------------------------------------

GLOBAL_CSS_BASE = """
<style>
/* =========================================================================
   DESIGN SYSTEM v2 — "Warm Academia"
   A Notion-inspired study tool with warm paper tones, amber accents,
   and a sophisticated warm-dark sidebar.
   ========================================================================= */

/* -------------------------------------------------------------------------
   CSS Variables
   ------------------------------------------------------------------------- */
:root {
    /* Main area — warm paper */
    --bg:                #faf9f7;
    --surface:           #ffffff;
    --surface-hover:     #f5f2ed;
    --input-bg:          #f3f0ec;
    --text:              #1c1b1a;
    --text-dim:          #78716c;
    --text-subtle:       #a8a29e;
    --border:            #e7e5e2;
    --border-light:      #f0eee9;

    /* Sidebar — warm dark charcoal */
    --sidebar-bg:        #1c1a17;
    --sidebar-surface:   #262320;
    --sidebar-hover:     #2f2c28;
    --sidebar-active:    #38342f;
    --sidebar-text:      #d4cfc8;
    --sidebar-text-dim:  #9d9690;
    --sidebar-border:    #2d2a26;

    /* Accent — amber/copper */
    --accent:            #d97706;
    --accent-light:      #fef3c7;
    --accent-hover:      #b45309;
    --accent-text:       #92400e;
    --accent-gradient:   linear-gradient(135deg, #d97706, #ea580c);

    /* Semantic */
    --success:           #059669;
    --success-bg:        #ecfdf5;
    --warning:           #d97706;
    --warning-bg:        #fffbeb;
    --error:             #dc2626;
    --error-bg:          #fef2f2;

    /* Shadows */
    --shadow-sm:   0 1px 2px rgba(0,0,0,0.04);
    --shadow-md:   0 2px 8px rgba(0,0,0,0.06);
    --shadow-lg:   0 4px 16px rgba(0,0,0,0.08);
    --shadow-xl:   0 8px 32px rgba(0,0,0,0.10);

    /* Radii */
    --radius-sm:  6px;
    --radius-md:  8px;
    --radius-lg:  12px;
    --radius-xl:  16px;

    /* Font */
    --font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI',
                    Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
}

/* -------------------------------------------------------------------------
   Base
   ------------------------------------------------------------------------- */
html {
    scroll-behavior: smooth;
}

body, .stApp {
    font-family: var(--font-family) !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* -------------------------------------------------------------------------
   Sidebar — warm dark
   ------------------------------------------------------------------------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1c1a17, #1f1d19) !important;
    border-right: 1px solid var(--sidebar-border);
}

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
    font-family: var(--font-family);
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2 {
    color: #f0ebe5 !important;
    font-weight: 600;
    letter-spacing: -0.02em;
}

section[data-testid="stSidebar"] h1 {
    font-size: 1.25rem;
    margin-bottom: 4px;
}

/* New Chat button (primary in sidebar) */
section[data-testid="stSidebar"] .stButton button[kind="primary"],
section[data-testid="stSidebar"] .stButton button[data-testid="baseButton-primary"] {
    background: var(--accent-gradient) !important;
    color: #ffffff !important;
    border: none;
    border-radius: var(--radius-md);
    font-weight: 600;
    font-size: 0.85rem;
    padding: 8px 16px;
    transition: all 150ms ease;
    box-shadow: 0 1px 3px rgba(217,119,6,0.2);
}
section[data-testid="stSidebar"] .stButton button[kind="primary"]:hover,
section[data-testid="stSidebar"] .stButton button[data-testid="baseButton-primary"]:hover {
    background: linear-gradient(135deg, #ea580c, #d97706) !important;
    box-shadow: 0 2px 8px rgba(217,119,6,0.3);
    transform: translateY(-1px);
}
section[data-testid="stSidebar"] .stButton button[kind="primary"] span,
section[data-testid="stSidebar"] .stButton button[data-testid="baseButton-primary"] span {
    color: #ffffff !important;
}

/* Secondary buttons */
section[data-testid="stSidebar"] .stButton button[kind="secondary"],
section[data-testid="stSidebar"] .stButton button[data-testid="baseButton-secondary"] {
    background-color: transparent;
    color: var(--sidebar-text) !important;
    border: 1px solid transparent;
    border-radius: var(--radius-sm);
    text-align: left;
    font-size: 0.82rem;
    padding: 6px 12px;
    transition: all 150ms ease;
}
section[data-testid="stSidebar"] .stButton button[kind="secondary"]:hover,
section[data-testid="stSidebar"] .stButton button[data-testid="baseButton-secondary"]:hover {
    background-color: var(--sidebar-hover);
    border-color: transparent;
}

/* Sidebar default buttons (e.g. Manage Files) */
section[data-testid="stSidebar"] .stButton button:not([kind="primary"]):not([kind="secondary"]) {
    background-color: var(--sidebar-surface);
    color: var(--sidebar-text) !important;
    border: 1px solid var(--sidebar-border);
    border-radius: var(--radius-md);
    font-size: 0.82rem;
    padding: 6px 8px;
    transition: all 150ms ease;
    line-height: 1.2;
}
section[data-testid="stSidebar"] .stButton button:not([kind="primary"]):not([kind="secondary"]):hover {
    background-color: var(--sidebar-hover);
    border-color: transparent;
}

/* Compact icon buttons in columns (rename/delete) */
section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] .stButton button {
    padding: 4px 6px !important;
    font-size: 0.8rem !important;
    min-height: 0 !important;
    line-height: 1.2;
}

/* Icon buttons (rename/delete) — compact sizing */
section[data-testid="stSidebar"] .stButton button[kind="secondary"] {
    padding: 4px 6px;
    font-size: 0.8rem;
    line-height: 1.2;
    min-height: 0;
}

/* Subject meta row inside expander (color dot visible when expanded) */
.subject-meta-row {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 4px 0 8px 0;
    margin-bottom: 8px;
    border-bottom: 1px solid var(--sidebar-border);
}
.subject-session-count {
    font-size: 0.75rem;
    color: var(--sidebar-text-dim);
}

/* Alert/info boxes in sidebar */
section[data-testid="stSidebar"] [data-testid="stAlert"] {
    background-color: var(--sidebar-surface) !important;
    border-radius: var(--radius-sm);
}
section[data-testid="stSidebar"] [data-testid="stAlertContainer"] {
    background-color: var(--sidebar-surface) !important;
    border-left-color: var(--accent) !important;
    border-radius: var(--radius-sm);
}
section[data-testid="stSidebar"] [data-testid="stAlert"] p,
section[data-testid="stSidebar"] [data-testid="stAlert"] span,
section[data-testid="stSidebar"] [data-testid="stAlert"] div,
section[data-testid="stSidebar"] [data-testid="stAlert"] a,
section[data-testid="stSidebar"] [data-testid="stAlertContainer"] p,
section[data-testid="stSidebar"] [data-testid="stAlertContainer"] span {
    color: var(--sidebar-text) !important;
}

/* Sidebar dividers */
section[data-testid="stSidebar"] hr {
    border-color: var(--sidebar-border) !important;
    opacity: 0.4;
    margin: 12px 0;
}
section[data-testid="stSidebar"] [data-testid="stMarkdown"] hr {
    border-color: var(--sidebar-border) !important;
}

/* Consistent spacing between sidebar elements */
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
    gap: 0.4rem !important;
}

/* Search input — consistent with button styling */
section[data-testid="stSidebar"] .stTextInput {
    margin-bottom: 0.25rem;
}
section[data-testid="stSidebar"] .stTextInput [data-testid="stTextInputRootElement"] {
    border-radius: var(--radius-md) !important;
}
section[data-testid="stSidebar"] .stTextInput [data-testid="stTextInputRootElement"] input {
    background-color: var(--sidebar-surface) !important;
    color: var(--sidebar-text) !important;
    border: 1px solid var(--sidebar-border) !important;
    border-radius: var(--radius-md) !important;
    font-size: 0.85rem;
    padding: 8px 12px;
    transition: border-color 150ms ease;
}
section[data-testid="stSidebar"] .stTextInput [data-testid="stTextInputRootElement"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(217,119,6,0.15);
}
section[data-testid="stSidebar"] .stTextInput [data-testid="stTextInputRootElement"] input::placeholder {
    color: var(--sidebar-text-dim) !important;
}

/* Buttons — consistent padding and alignment */
section[data-testid="stSidebar"] .stButton {
    margin-bottom: 0.15rem;
}
section[data-testid="stSidebar"] .stButton button {
    border-radius: var(--radius-md) !important;
    font-size: 0.85rem;
}

/* Expanders — consistent with buttons */
section[data-testid="stSidebar"] [data-testid="stExpander"] {
    border: none !important;
    margin-bottom: 0.15rem;
}
section[data-testid="stSidebar"] [data-testid="stExpander"] details {
    border: 1px solid var(--sidebar-border) !important;
    border-radius: var(--radius-md) !important;
    background-color: transparent;
}
section[data-testid="stSidebar"] [data-testid="stExpander"] summary {
    color: var(--sidebar-text) !important;
    background-color: transparent !important;
    font-weight: 600;
    font-size: 0.85rem;
    padding: 8px 12px;
    border-radius: var(--radius-md);
    transition: background-color 150ms ease;
}
section[data-testid="stSidebar"] [data-testid="stExpander"] summary:hover {
    background-color: var(--sidebar-hover) !important;
}
section[data-testid="stSidebar"] [data-testid="stExpanderDetails"] {
    background-color: transparent !important;
    border-top-color: var(--sidebar-border) !important;
    padding: 4px 8px;
}

/* Markdown in sidebar */
section[data-testid="stSidebar"] [data-testid="stMarkdown"] p,
section[data-testid="stSidebar"] [data-testid="stMarkdown"] span,
section[data-testid="stSidebar"] [data-testid="stMarkdown"] li,
section[data-testid="stSidebar"] [data-testid="stMarkdown"] a,
section[data-testid="stSidebar"] [data-testid="stMarkdown"] code {
    color: var(--sidebar-text) !important;
}
section[data-testid="stSidebar"] [data-testid="stMarkdown"] a {
    color: var(--accent) !important;
}
section[data-testid="stSidebar"] [data-testid="stMarkdown"] a:hover {
    color: var(--accent-hover) !important;
}

/* Slider labels */
section[data-testid="stSidebar"] .stSlider [data-testid="stWidgetLabel"] {
    color: var(--sidebar-text) !important;
    font-size: 0.78rem;
    font-weight: 500;
}
section[data-testid="stSidebar"] .stSlider [data-testid="stSliderThumbValue"] {
    color: var(--sidebar-text) !important;
    font-size: 0.75rem;
}
section[data-testid="stSidebar"] .stSlider [data-testid="stSliderTickBar"] {
    color: var(--sidebar-text-dim) !important;
}

/* Checkbox (Search All toggle) */
section[data-testid="stSidebar"] .stCheckbox label {
    color: var(--sidebar-text) !important;
    font-size: 0.82rem;
}
section[data-testid="stSidebar"] .stCheckbox [data-testid="stWidgetLabel"] {
    color: var(--sidebar-text) !important;
}

/* Caption text */
section[data-testid="stSidebar"] [data-testid="stCaption"] {
    color: var(--sidebar-text-dim) !important;
    font-size: 0.75rem;
}

/* Download buttons */
section[data-testid="stSidebar"] .stDownloadButton button {
    background-color: var(--sidebar-surface);
    color: var(--sidebar-text) !important;
    border: 1px solid var(--sidebar-border);
    border-radius: var(--radius-md);
    font-size: 0.82rem;
    transition: all 150ms ease;
}
section[data-testid="stSidebar"] .stDownloadButton button:hover {
    background-color: var(--sidebar-hover);
}

/* -------------------------------------------------------------------------
   Top bar — sticky header (no :has() selector for Streamlit compat)
   ------------------------------------------------------------------------- */
.glass-top-bar {
    position: sticky;
    top: 0;
    z-index: 100;
    background: rgba(255, 255, 255, 0.94);
    border-bottom: 1px solid var(--border);
    padding: 6px 0;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.top-bar-title {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text);
    letter-spacing: -0.01em;
}

.top-bar-divider {
    color: var(--text-subtle);
    font-size: 1.2rem;
    font-weight: 300;
}

.top-bar-session {
    font-size: 0.85rem;
    color: var(--text-dim);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

/* -------------------------------------------------------------------------
   User messages — white card with amber accent border
   ------------------------------------------------------------------------- */
.user-message {
    background: var(--surface);
    border-left: 4px solid var(--accent);
    border-radius: var(--radius-lg);
    padding: 14px 18px;
    margin: 12px 0 12px 48px;
    margin-right: 0;
    max-width: 78%;
    box-shadow: var(--shadow-sm);
    font-size: 0.9375rem;
    line-height: 1.6;
    color: var(--text);
    float: right;
    clear: both;
}

/* -------------------------------------------------------------------------
   Assistant messages — white card
   ------------------------------------------------------------------------- */
.assistant-message {
    background: var(--surface);
    border-radius: var(--radius-lg);
    padding: 16px 20px;
    margin: 12px 0;
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border);
    font-size: 0.9375rem;
    line-height: 1.6;
    color: var(--text);
    position: relative;
    clear: both;
}

.assistant-content {
    white-space: pre-wrap;
    word-wrap: break-word;
}

.assistant-content p {
    margin: 0 0 8px 0;
}
.assistant-content p:last-child {
    margin-bottom: 0;
}

/* Copy button (hover reveal) */
.message-actions {
    display: none;
    position: absolute;
    top: 12px;
    right: 12px;
    z-index: 2;
}
.assistant-message:hover .message-actions {
    display: block;
}
.copy-btn {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 4px 10px;
    font-size: 0.72rem;
    color: var(--text-dim);
    cursor: pointer;
    transition: all 150ms ease;
    font-family: var(--font-family);
}
.copy-btn:hover {
    background: var(--surface-hover);
    color: var(--text);
    border-color: var(--accent);
}

/* -------------------------------------------------------------------------
   Citation pills — amber
   ------------------------------------------------------------------------- */
.citation-pill {
    display: inline-block;
    background-color: var(--accent);
    color: #ffffff;
    font-size: 0.68rem;
    font-weight: 600;
    padding: 1px 7px;
    border-radius: 10px;
    cursor: pointer;
    margin: 0 2px;
    vertical-align: super;
    transition: background-color 150ms ease;
    user-select: none;
}
.citation-pill:hover {
    background-color: var(--accent-hover);
}

/* -------------------------------------------------------------------------
   Source chunks
   ------------------------------------------------------------------------- */
.source-chunk {
    background-color: #fffbeb;
    border-left: 3px solid var(--accent);
    border-radius: 0 var(--radius-md) var(--radius-md) 0;
    padding: 10px 14px;
    margin: 8px 0;
    font-size: 0.82rem;
    color: var(--text);
    line-height: 1.5;
}
.source-chunk .source-label {
    font-weight: 600;
    color: var(--accent);
    font-size: 0.78rem;
    margin-bottom: 4px;
}

/* -------------------------------------------------------------------------
   Input bar
   ------------------------------------------------------------------------- */
div[data-testid="stChatInput"] {
    border-radius: var(--radius-lg);
    background-color: var(--surface);
    border: 1px solid var(--border);
    box-shadow: var(--shadow-sm);
    transition: all 150ms ease;
}
div[data-testid="stChatInput"]:focus-within {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px rgba(217,119,6,0.10), var(--shadow-md);
}
div[data-testid="stChatInput"] textarea {
    font-size: 0.9375rem;
    font-family: var(--font-family);
    color: var(--text);
    line-height: 1.5;
}
div[data-testid="stChatInput"] textarea::placeholder {
    color: var(--text-subtle);
}
.stChatInput {
    border-radius: var(--radius-lg);
}

button[data-testid="stChatInput-send"] {
    background: var(--accent-gradient) !important;
    border-radius: var(--radius-sm) !important;
    color: white !important;
    transition: all 150ms ease !important;
}
button[data-testid="stChatInput-send"]:hover {
    transform: scale(1.05);
    box-shadow: 0 2px 8px rgba(217,119,6,0.3);
}

button[kind="tertiary"] {
    color: var(--text-dim) !important;
    transition: color 150ms ease !important;
}
button[kind="tertiary"]:hover {
    color: var(--accent) !important;
}

/* -------------------------------------------------------------------------
   Settings
   ------------------------------------------------------------------------- */
.search-all-wrapper {
    padding: 8px 0;
    margin-bottom: 8px;
}

/* -------------------------------------------------------------------------
   Suggested questions
   ------------------------------------------------------------------------- */
.suggested-section {
    text-align: center;
    margin-top: 48px;
    margin-bottom: 24px;
}
.suggested-label {
    font-size: 0.85rem;
    color: var(--text-dim);
    font-weight: 500;
    margin-bottom: 16px;
}

.suggested-question {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 12px 18px;
    cursor: pointer;
    font-size: 0.88rem;
    color: var(--text);
    margin: 6px 0;
    transition: all 150ms ease;
    box-shadow: var(--shadow-sm);
    text-align: left;
    font-family: var(--font-family);
    width: 100%;
}
.suggested-question:hover {
    border-color: var(--accent);
    background: #fffbeb;
    box-shadow: 0 2px 8px rgba(217,119,6,0.10);
    transform: translateY(-1px);
}

.suggested-question-btn {
    text-align: left !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
}

/* -------------------------------------------------------------------------
   Empty / welcome states
   ------------------------------------------------------------------------- */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 80px 24px;
}
.empty-state-icon {
    font-size: 3rem;
    margin-bottom: 16px;
    opacity: 0.7;
}
.empty-state h2 {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 8px;
    letter-spacing: -0.02em;
}
.empty-state p {
    font-size: 0.95rem;
    color: var(--text-dim);
    max-width: 400px;
    line-height: 1.5;
}
.empty-state code {
    background: var(--surface-hover);
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.85rem;
    color: var(--accent);
}
.empty-state .accent-text {
    color: var(--accent);
    font-weight: 500;
}

/* -------------------------------------------------------------------------
   Artifact panel
   ------------------------------------------------------------------------- */
.artifact-panel {
    background-color: #faf9f7;
    border-left: 1px solid var(--border);
    padding: 20px 20px 20px 24px;
    min-height: calc(100vh - 40px);
    border-radius: var(--radius-xl) 0 0 var(--radius-xl);
}

.artifact-panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 12px;
    border-bottom: 2px solid var(--accent);
    margin-bottom: 16px;
}
.artifact-panel-header h3 {
    margin: 0;
    font-size: 1rem;
    font-weight: 600;
    color: var(--text);
}

.artifact-close-btn {
    background: transparent;
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 4px 10px;
    cursor: pointer;
    color: var(--text-dim);
    font-size: 0.82rem;
    transition: all 150ms ease;
    font-family: var(--font-family);
}
.artifact-close-btn:hover {
    background: var(--surface-hover);
    color: var(--error);
    border-color: var(--error);
}

.artifact-copy-btn {
    background: transparent;
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 6px 12px;
    cursor: pointer;
    font-size: 0.82rem;
    color: var(--text);
    width: 100%;
    transition: all 150ms ease;
    font-family: var(--font-family);
}
.artifact-copy-btn:hover {
    background: var(--surface-hover);
    border-color: var(--accent);
}

.artifact-content {
    font-size: 0.9rem;
    line-height: 1.65;
    color: var(--text);
}
.artifact-content h1,
.artifact-content h2,
.artifact-content h3 {
    font-weight: 600;
    color: var(--text);
    margin-top: 20px;
    margin-bottom: 8px;
}

/* Artifact panel markdown (from st.markdown) */
.artifact-panel [data-testid="stMarkdown"] {
    font-size: 0.9rem;
    line-height: 1.65;
    color: var(--text);
}
.artifact-panel [data-testid="stMarkdown"] h1,
.artifact-panel [data-testid="stMarkdown"] h2,
.artifact-panel [data-testid="stMarkdown"] h3 {
    font-weight: 600;
    color: var(--text);
    margin-top: 20px;
    margin-bottom: 8px;
}
.artifact-panel [data-testid="stMarkdown"] table {
    border-collapse: collapse;
    width: 100%;
    margin: 12px 0;
    font-size: 0.85rem;
}
.artifact-panel [data-testid="stMarkdown"] th,
.artifact-panel [data-testid="stMarkdown"] td {
    border: 1px solid var(--border);
    padding: 8px 12px;
    text-align: left;
}
.artifact-panel [data-testid="stMarkdown"] th {
    background: var(--bg);
    font-weight: 600;
}
.artifact-panel [data-testid="stMarkdown"] code {
    background: var(--surface-hover);
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.82rem;
    color: var(--accent-text);
}
.artifact-panel [data-testid="stMarkdown"] pre code {
    display: block;
    padding: 12px 16px;
    overflow-x: auto;
}

.artifact-action-bar {
    display: flex;
    gap: 8px;
    margin-bottom: 16px;
}
.artifact-action-bar button,
.artifact-action-bar .stButton button {
    flex: 1;
    font-size: 0.82rem;
    border-radius: var(--radius-sm);
    transition: all 150ms ease;
}
.artifact-action-bar .stDownloadButton button {
    border-radius: var(--radius-sm);
    font-size: 0.82rem;
}

/* Artifact list in sidebar */
.artifact-list-item-wrapper {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 4px 4px;
    border-radius: var(--radius-sm);
    transition: background-color 150ms ease;
}
.artifact-list-item-wrapper:hover {
    background-color: var(--sidebar-hover);
}

.artifact-type-badge {
    display: inline-block;
    font-size: 0.62rem;
    font-weight: 600;
    padding: 2px 6px;
    border-radius: 4px;
    background: var(--accent-gradient);
    color: white;
    text-transform: uppercase;
    letter-spacing: 0.03em;
    flex-shrink: 0;
}

.artifact-name-text {
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-size: 0.78rem;
    color: var(--sidebar-text);
}

/* -------------------------------------------------------------------------
   File Manager
   ------------------------------------------------------------------------- */
.file-card {
    display: flex;
    align-items: center;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 10px 14px;
    margin: 6px 0;
    transition: all 150ms ease;
}
.file-card:hover {
    border-color: var(--text-subtle);
    box-shadow: var(--shadow-sm);
}

.file-card-icon {
    font-size: 1.2rem;
    margin-right: 12px;
    flex-shrink: 0;
}

.file-card-name {
    flex: 1;
    font-weight: 500;
    font-size: 0.88rem;
    color: var(--text);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.file-card-size {
    font-size: 0.75rem;
    color: var(--text-dim);
    margin-right: 12px;
    white-space: nowrap;
}

.file-status-pill {
    display: inline-block;
    font-size: 0.68rem;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 10px;
    background: transparent;
    white-space: nowrap;
}
.file-status-pill.indexed {
    background: var(--success-bg);
    color: var(--success);
}
.file-status-pill.not-indexed {
    background: var(--warning-bg);
    color: var(--warning);
}

/* Upload modal */
.dialog-upload-area {
    border: 2px dashed var(--border);
    border-radius: var(--radius-lg);
    padding: 32px;
    text-align: center;
    background: var(--bg);
    transition: border-color 150ms ease;
}
.dialog-upload-area:hover {
    border-color: var(--accent);
}

/* Rebuild section */
.rebuild-section .stButton button {
    border-radius: var(--radius-md);
    transition: all 150ms ease;
}

/* Select chat placeholder */
.select-chat-placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 400px;
    text-align: center;
    color: var(--text-subtle);
    font-size: 0.95rem;
}
</style>
"""

# ---------------------------------------------------------------------------
# ENHANCED CSS — animations, scrollbar, progress bar, responsive.
# Injected separately. If this block fails, the base styles still work.
# ---------------------------------------------------------------------------

GLOBAL_CSS_ENHANCED = """
<style>
/* =========================================================================
   ENHANCED STYLES
   Progressive enhancements: animations, custom scrollbar, progress bars,
   responsive breakpoints. Graceful degradation if unsupported.
   ========================================================================= */

/* -------------------------------------------------------------------------
   Animations
   ------------------------------------------------------------------------- */
@keyframes messageIn {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}

.user-message {
    animation: messageIn 0.2s ease;
}
.assistant-message {
    animation: messageIn 0.25s ease;
}
.empty-state,
.suggested-section,
.artifact-panel {
    animation: fadeIn 0.4s ease;
}

/* -------------------------------------------------------------------------
   Scrollbar
   ------------------------------------------------------------------------- */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: transparent;
}
::-webkit-scrollbar-thumb {
    background: #c5bfb880;
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: #a8a29e;
}
* {
    scrollbar-width: thin;
    scrollbar-color: #c5bfb880 transparent;
}

/* -------------------------------------------------------------------------
   Progress bar
   ------------------------------------------------------------------------- */
.stProgress > div > div > div > div {
    background: var(--accent-gradient) !important;
}

/* -------------------------------------------------------------------------
   Status messages
   ------------------------------------------------------------------------- */
.stAlert {
    border-radius: var(--radius-md) !important;
}
div[data-testid="stNotification"] {
    border-radius: var(--radius-md) !important;
}

/* -------------------------------------------------------------------------
   Responsive — 768px
   ------------------------------------------------------------------------- */
@media (max-width: 768px) {
    section[data-testid="stSidebar"] {
        max-width: 260px !important;
    }

    .user-message {
        margin-left: 16px;
        max-width: 92%;
        float: none;
    }

    .assistant-message {
        margin-left: 0;
        margin-right: 0;
    }

    .empty-state {
        padding: 48px 16px;
    }

    .empty-state h2 {
        font-size: 1.25rem;
    }

    .top-bar-title {
        font-size: 0.9rem;
    }

    .top-bar-session {
        display: none;
    }

    .artifact-panel {
        padding: 12px;
    }

    .file-card {
        flex-wrap: wrap;
        gap: 6px;
    }

    .file-card-size {
        width: 100%;
        margin-right: 0;
    }

    .suggested-section {
        margin-top: 32px;
    }
}

/* -------------------------------------------------------------------------
   Responsive — 480px
   ------------------------------------------------------------------------- */
@media (max-width: 480px) {
    .user-message {
        margin-left: 8px;
        max-width: 95%;
        padding: 10px 14px;
    }

    .assistant-message {
        padding: 12px 14px;
    }

    .empty-state {
        padding: 32px 12px;
    }
}
</style>
"""
