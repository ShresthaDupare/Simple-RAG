# Study RAG Assistant — Master Plan

> **This is the living document for the project.** All design decisions, features, and changes are tracked here. Update this file whenever features are added, removed, or modified.

**Last updated:** 2026-06-25 (Phase 10 complete)

---

## Overview

A Streamlit web app with a ChatGPT/Claude-hybrid UI for querying study material organized by subject. Uses DeepSeek API for LLM, FAISS for vector search, and sentence-transformers for local embeddings.

---

## Tech Stack

| Component | Choice | Why |
|-----------|--------|-----|
| UI | Streamlit | User preference |
| LLM | DeepSeek API (OpenAI-compatible) | User has API key |
| Vector Store | FAISS | Local, fast, no server |
| Embeddings | `sentence-transformers` (`all-MiniLM-L6-v2`) | Free, local, no API |
| Doc Loading | `pypdf` + `python-pptx` | Handles PDF & PPTX |
| Orchestration | `langchain` | Ties everything together |

**DeepSeek config:**
- Base URL: `https://api.deepseek.com`
- Model: `deepseek-chat`
- Uses `openai` Python SDK with `base_url` override

---

## Design Decisions

| Decision | Choice |
|----------|--------|
| App type | Streamlit web app |
| Theme | Dark sidebar + light main area |
| Messages | Hybrid — user bubbles (light indigo), assistant plain text (ChatGPT-style) |
| Layout | Responsive (collapses sidebar on mobile) |
| Subject management | Folder-only (manual), auto-detected from `data/` subfolders |
| Chat sessions | Multiple per subject (like ChatGPT conversation list) |
| Search | Per-subject + "Search All" toggle |
| Artifacts | Slash commands, right slide-in panel, persisted to disk |

---

## UI Design — v1 (Original)

### Visual Style: ChatGPT + Claude Hybrid

**Color Palette (v1 — replaced 2026-06-26):**

| Element | v1 Color | v2 Replacement |
|---------|----------|----------------|
| Background | `#ffffff` | `#faf9f7` (warm paper) |
| Sidebar bg | `#1a1a2e` (cold navy) | `#1c1a17` (warm charcoal) |
| Sidebar text | `#e0e0e0` | `#d4cfc8` (warm light) |
| Sidebar hover | `#2a2a4a` | `#2f2c28` |
| Sidebar active | `#3a3a5a` | `#38342f` |
| Primary accent | `#6366f1` (indigo) | `#d97706` (amber/copper) |
| User message bg | `#f0f0ff` (barely visible) | `#fef3c7` (amber tint bubble) |
| Assistant message | `#ffffff` (no container) | White card with shadow + border |
| Citation pills | `#6366f1` on `#f0f0ff` | `#d97706` amber pills, white text |
| Input bg | `#f7f7f8` | `#ffffff` (card) |
| Input border | `#e5e5e5` | `#e7e5e2` (warm) |
| Send button | `#6366f1` | Amber gradient `#d97706 → #ea580c` |
| Text | `#1a1a2e` | `#1c1b1a` (rich warm dark) |
| Subtle text | `#888888` | `#78716c` (warm muted) |

### Layout Structure

```
┌──────────────────────────────────────────────────────────────────────┐
│ ┌─SIDEBAR──┐  ┌─MAIN CHAT AREA──────────────────────────────────┐   │
│ │           │  │                                                 │   │
│ │ 📚 Study  │  │  ┌─TOP BAR──────────────────────────────────┐  │   │
│ │   RAG     │  │  │ Subject / Session Name             [⋮]  │  │   │
│ │           │  │  └─────────────────────────────────────────┘  │   │
│ │ [Search]  │  │                                                 │   │
│ │           │  │         (centered column, max 750px)            │   │
│ │ [+ New]   │  │                                                 │   │
│ │           │  │  User messages: indigo bubble, right-ish        │   │
│ │ ▾ Subject │  │  Assistant messages: plain text, left-aligned   │   │
│ │   Chat 1  │  │  Citations: clickable pills [1] [2] [3]        │   │
│ │   Chat 2  │  │  Sources: expandable inline chunks              │   │
│ │           │  │                                                 │   │
│ │ ▾ Subject │  │                                                 │   │
│ │   Chat 1  │  │  ┌──────────────────────────────────────┐ [📎] │   │
│ │           │  │  │ Ask about [subject]...            ➤  │       │   │
│ │           │  │  └──────────────────────────────────────┘       │   │
│ │ ⚙ Settings│  │                                                 │   │
│ └───────────┘  └─────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────┘
```

### Sidebar Sections

1. **App title:** `📚 Study RAG`
2. **Search bar:** Filter sessions by name
3. **+ New Chat button**
4. **Subject groups** (collapsible):
   - Subject header with colored dot indicator
   - List of chat sessions under each subject
   - Active session highlighted
   - Hover: rename/delete icons
5. **Settings** (collapsible at bottom):
   - Top-K slider (1–10, default 4)
   - Max history turns slider (1–20, default 5)
   - Temperature slider (0–1, default 0.3)
   - Chunk size slider (500–2000, default 1000)
   - Chunk overlap slider (50–500, default 200)

### Message Styling

- **User messages:** Light indigo bubble (`#f0f0ff`), rounded corners, slightly right-aligned
- **Assistant messages:** Plain text, no bubble, left-aligned, with copy button on hover
- **Citations:** Inline pills `[1]` `[2]` that expand source text on click
- **Source chunks:** Show file name + page/slide, expandable to see full retrieved text

### Input Bar

- Floating at bottom with subtle shadow
- Rounded text area, auto-resizes up to 4 lines
- Attachment button (left) for file upload
- Send button (right)
- Enter = send, Shift+Enter = new line
- Placeholder adapts to current subject name

### Responsive Behavior

- On narrow screens, sidebar collapses to icons only
- Hamburger menu to expand sidebar
- Chat area fills full width when sidebar collapsed

---

## Features (Complete List)

### Core

| # | Feature | Description |
|---|---------|-------------|
| 1 | Auto-detect subjects | Scans `data/` subfolders, no UI creation needed |
| 2 | Subject selector | Dropdown to switch between subjects |
| 3 | Per-subject index | Each subject gets its own FAISS index |
| 4 | Search All toggle | Option to query all subject indices at once |

### Chat

| # | Feature | Description |
|---|---------|-------------|
| 5 | Multiple chat sessions | Per-subject, like ChatGPT sidebar |
| 6 | New / rename / delete sessions | Full session management |
| 7 | Multi-turn conversation | Last N messages sent as context |
| 8 | Streaming responses | Token-by-token from DeepSeek |
| 9 | Source citations | File name + page/slide per source |
| 10 | Expandable sources | Click to see retrieved chunk text |
| 11 | Chat persistence | Per-subject JSON, survives restarts |
| 12 | Suggested questions | Shown for new empty sessions |
| 13 | Copy answer | One-click copy button per message |
| 14 | Clear chat | Reset current session |

### Files

| # | Feature | Description |
|---|---------|-------------|
| 15 | File upload | Scoped to current subject's folder |
| 16 | File list | Shows files in subject with delete option |
| 17 | Rebuild index | Per-subject, with progress bar |

### UI

| # | Feature | Description |
|---|---------|-------------|
| 18 | Dark sidebar + light main | ChatGPT/Claude hybrid style |
| 19 | Responsive layout | Collapses on mobile/tablet |

### Artifacts

| # | Feature | Description |
|---|---------|-------------|
| 20 | `/summary <file>` | Document summary |
| 21 | `/glossary <file>` | Key terms extraction |
| 22 | `/compare <topic>` | Comparison tables across documents |
| 23 | `/explain <topic>` | Explanations/walkthroughs |
| 24 | Right slide-in panel | Artifact display (like Claude) |
| 25 | Slash command autocomplete | `/` shows commands, then file picker |
| 26 | Copy artifact | Copy full markdown to clipboard |
| 27 | Download artifact | Download as `.md` file |
| 28 | Persist artifacts | Saved to `artifacts/<subject>/` |
| 29 | Artifact list in sidebar | Clickable list of saved artifacts |

---

## Artifact System

### Slash Commands

| Command | What It Does |
|---------|--------------|
| `/summary <filename>` | Condensed summary of the entire document |
| `/glossary <filename>` | Key terms with definitions as a table |
| `/compare <topic>` | Compares concepts across documents in the subject |
| `/explain <topic>` | Step-by-step walkthrough of a concept |

### Artifact Prompts

**Summary:**
```
You are a study assistant. Create a comprehensive summary of the following document.
Include:
- Main topic and purpose
- Key concepts (with brief explanations)
- Important facts, formulas, or definitions
- Section-by-section breakdown if applicable
Format in clean Markdown with headers and bullet points.

Document: {full_text}
```

**Glossary:**
```
You are a study assistant. Extract all key terms and their definitions from
the following document. Format as a Markdown table:
| Term | Definition |
|------|------------|
Include only technical/important terms. Be concise but accurate.

Document: {full_text}
```

**Comparison:**
```
You are a study assistant. Based on the following documents about {topic},
create comparison tables that highlight:
- Similarities and differences between concepts
- Pros and cons where applicable
- Key distinguishing features
Format as clean Markdown tables.

Documents: {relevant_chunks_from_all_files}
```

**Explanation:**
```
You are a study assistant. Provide a detailed, step-by-step explanation of
{topic} based on the following material. Include:
- Clear sequential steps
- Examples where possible
- Common misconceptions to avoid
Format in clean Markdown.

Context: {relevant_chunks}
```

### Artifact Storage

Each artifact saved as `.md` with YAML front matter:

```markdown
---
type: summary
source_file: FES-in-Rehab.pptx
subject: Rehabilitation Engineering
created_at: 2026-06-22T14:30:00
---

# Summary: FES-in-Rehab.pptx

Content here...
```

### Artifact Panel Behavior

| Action | Result |
|--------|--------|
| Artifact generated | Panel slides in from right, streams content |
| Click **✕** | Panel closes, chat expands back |
| Click **📋 Copy** | Copies full markdown to clipboard |
| Click **⬇️ Download** | Downloads as `.md` file |
| Generate new artifact | Previous replaced in panel (but saved to disk) |
| Switch chat session | Panel closes |

---

## File Structure

```
Simple RAG/
├── PLAN.md                     # This file — living project plan
├── todo.md                     # Feature tracker with checkboxes per phase
├── requirements.txt            # All dependencies
├── .env                        # DEEPSEEK_API_KEY=sk-...
├── .gitignore
├── app.py                      # Root entry point for Streamlit Community Cloud
│
├── .streamlit/                 # Streamlit configuration
│   └── config.toml             # Server + theme settings
│
├── src/                        # All source code (maintainability-first structure)
│   ├── __init__.py
│   ├── config.py               # Settings, env loading, constants, path helpers
│   ├── models.py               # Dataclasses: ChatMessage, Session, Artifact, SourceChunk
│   ├── exceptions.py           # Custom exceptions for clear error handling
│   │
│   ├── loaders/                # Document loading (split by format)
│   │   ├── __init__.py         # Dispatcher: load_document(), load_and_chunk()
│   │   ├── scanner.py          # scan_subjects(), get_files()
│   │   ├── pdf_loader.py       # load_pdf(), load_full_pdf()
│   │   └── pptx_loader.py      # load_pptx(), load_full_pptx()
│   │
│   ├── retrieval/              # RAG components
│   │   ├── __init__.py
│   │   ├── embeddings.py       # Sentence-transformer wrapper (singleton)
│   │   ├── vector_store.py     # FAISS create/load/search/search-all
│   │   └── rag_chain.py        # Prompt building + DeepSeek streaming
│   │
│   ├── storage/                # Persistence layer
│   │   ├── __init__.py
│   │   ├── chat_store.py       # JSON CRUD for sessions
│   │   └── artifact_store.py   # Artifact file read/write/list
│   │
│   ├── artifacts/              # Artifact generation
│   │   ├── __init__.py
│   │   ├── prompts.py          # All artifact prompt templates
│   │   ├── parser.py           # Slash command parsing
│   │   └── generator.py        # Streaming artifact generation
│   │
│   └── ui/                     # Streamlit UI (split by component)
│       ├── __init__.py
│       ├── app.py              # Main entry, session state, routing
│       ├── sidebar.py          # Sidebar rendering + settings sliders
│       ├── chat.py             # Chat display + input + streaming + citations
│       ├── artifacts_panel.py  # Artifact slide-in panel + slash commands
│       ├── file_manager.py     # Upload, list, delete files + rebuild index
│       └── styles.py           # All CSS in one place (Streamlit 1.58.0)
│
├── data/                       # User creates subject folders here
│   └── .gitkeep
│
├── faiss_index/                # Auto-created per subject
│   └── .gitkeep
│
├── chat_history/               # Auto-created, one JSON per subject
│   └── .gitkeep
│
└── artifacts/                  # Persisted artifact markdown files
    └── .gitkeep
```

---

## Dependencies (requirements.txt)

```
streamlit>=1.30.0
langchain>=0.2.0
langchain-community>=0.2.0
langchain-text-splitters>=0.2.0
faiss-cpu>=1.7.4
sentence-transformers>=2.2.0
pypdf>=4.0.0
python-pptx>=0.6.21
openai>=1.0.0
python-dotenv>=1.0.0
```

---

## File Responsibilities

| File | Purpose | ~Lines | Status |
|------|---------|--------|--------|
| `src/config.py` | Settings, env loading, constants, path helpers | ~94 | Done |
| `src/models.py` | Dataclasses: ChatMessage, Session, Artifact, SourceChunk | ~134 | Done |
| `src/exceptions.py` | Custom exceptions for clear error paths | ~52 | Done |
| `src/loaders/scanner.py` | Scan subjects, list files | ~69 | Done |
| `src/loaders/pdf_loader.py` | PDF → chunks + full text | ~72 | Done |
| `src/loaders/pptx_loader.py` | PPTX → chunks + full text | ~86 | Done |
| `src/loaders/__init__.py` | Dispatcher, load_and_chunk() | ~126 | Done |
| `src/retrieval/embeddings.py` | Sentence-transformer wrapper | ~52 | Done |
| `src/retrieval/vector_store.py` | FAISS create/load/search/search-all | ~213 | Done |
| `src/retrieval/rag_chain.py` | Prompt building + DeepSeek streaming | ~219 | Done |
| `src/storage/chat_store.py` | JSON CRUD for sessions | ~99 | Done |
| `src/storage/artifact_store.py` | Artifact file management | ~114 | Done |
| `src/artifacts/prompts.py` | All artifact prompt templates | ~48 | Done |
| `src/artifacts/parser.py` | Slash command parsing | ~85 | Done |
| `src/artifacts/generator.py` | Streaming artifact generation | ~122 | Done |
| `src/ui/styles.py` | All CSS (injected via JS component) | ~1077 | Done |
| `src/ui/app.py` | Main entry, session state, routing | ~141 | Done |
| `src/ui/sidebar.py` | Sidebar rendering + settings sliders | ~287 | Done |
| `src/ui/chat.py` | Chat display + input + streaming + citations | ~373 | Done |
| `src/ui/artifacts_panel.py` | Artifact slide-in panel + slash commands | ~268 | Done |
| `src/ui/file_manager.py` | Upload, list, delete files + rebuild index | ~207 | Done |
| `src/ui/css_injector.py` | JS-based CSS injection component | ~38 | Done |

**Total: ~4021 lines across 27 files.**

---

## Implementation Steps

> **Progress is tracked in `todo.md`.** Each phase has checkboxes. Update `todo.md` as you complete work.

### Phase 0: Project Setup ✅ DONE
- Create `requirements.txt`, `.env`, `.gitignore`
- Create `src/` folder structure with `__init__.py` files
- Create empty data directories with `.gitkeep`

### Phase 1: Config & Models ✅ DONE
- `src/config.py` — load `.env`, define all constants, paths, defaults
- `src/models.py` — dataclasses for type-safe data structures
- `src/exceptions.py` — custom exceptions for clear error handling

### Phase 2: Document Loading ✅ DONE
- `src/loaders/scanner.py` — `scan_subjects()`, `get_files()`
- `src/loaders/pdf_loader.py` — PDF loading with metadata
- `src/loaders/pptx_loader.py` — PPTX loading with metadata
- `src/loaders/__init__.py` — dispatcher + `load_and_chunk()` with text splitter

### Phase 3: Embeddings & Vector Store ✅ DONE
- `src/retrieval/embeddings.py` — sentence-transformer singleton wrapper
- `src/retrieval/vector_store.py` — FAISS create/load/search/search-all

### Phase 4: RAG Chain ✅ DONE
- `src/retrieval/rag_chain.py` — system prompt, build_prompt(), call_deepseek_stream()

### Phase 5: Storage ✅ DONE
- `src/storage/chat_store.py` — JSON CRUD for sessions
- `src/storage/artifact_store.py` — artifact file management

### Phase 6: Artifacts ✅ DONE
- `src/artifacts/prompts.py` — prompt templates
- `src/artifacts/parser.py` — slash command parsing
- `src/artifacts/generator.py` — streaming generation

### Phase 7: UI Setup ✅ DONE
- `src/ui/styles.py` — all CSS
- `src/ui/app.py` — page config, session state, routing
- `src/ui/sidebar.py` — sidebar rendering

### Phase 8: Chat UI ✅ DONE
- `src/ui/chat.py` — messages, input, streaming, citations

### Phase 9: File Manager UI ✅ DONE
- `src/ui/file_manager.py` — upload, list, delete, rebuild index

### Phase 10: Artifacts UI ✅ DONE
- `src/ui/artifacts_panel.py` — slide-in panel, slash commands, autocomplete, streaming, copy, download
- `src/ui/chat.py` — full slash command handling with artifact generation
- `src/ui/sidebar.py` — artifact list in sidebar
- `src/ui/styles.py` — artifact panel CSS

### Phase 11: Final Polish (Pending)
- Responsive CSS, suggested questions, Search All toggle

### Phase 12: Final Testing (Pending)
- Full workflow verification

---

## Progress Tracking with todo.md

**`todo.md` is the single source of truth for implementation progress.** It contains:

1. **Phase-based checklist** — Each phase (0–12) has checkboxes for every task
2. **Completed Features table** — Date, phase, and files created/modified
3. **Notes section** — Run commands and prerequisites

### How to use todo.md:

- **When starting work:** Read todo.md to see what's pending
- **When completing a task:** Check off the item with `- [x]`
- **When completing a phase:** Update the Completed Features table
- **When starting a new phase:** The next unchecked phase is your starting point

### Why separate from PLAN.md?

- **PLAN.md** = Design decisions, architecture, what we're building
- **todo.md** = Implementation progress, what's done vs pending

This separation keeps PLAN.md clean as a reference document while todo.md serves as a working checklist.

---

## Chat History JSON Schema

```json
{
  "sessions": {
    "uuid-1": {
      "name": "FES Overview",
      "created_at": "2026-06-22T10:00:00",
      "messages": [
        {
          "role": "user",
          "content": "What is FES?",
          "sources": [],
          "timestamp": "2026-06-22T10:00:01"
        },
        {
          "role": "assistant",
          "content": "FES is a technique that uses...",
          "sources": [
            {
              "content": "FES uses electrical currents to stimulate...",
              "source": "FES-in-Rehab.pptx",
              "page": 3,
              "score": 0.85
            }
          ],
          "timestamp": "2026-06-22T10:00:05"
        }
      ]
    }
  }
}
```

---

## Run Command

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Pre-requisites

1. **DeepSeek API key** — paste into `.env` as `DEEPSEEK_API_KEY=sk-...`
2. **Study files** — create subject folders in `data/` and copy PDFs/PPTX there
3. **Python 3.9+** installed

---

## Design System v2 — "Warm Academia" (2026-06-26)

> **Complete UI redesign.** All visual styles were overhauled for a modern, polished look.
> Colors, typography, spacing, shadows, and component styles were all redesigned.
> Zero functional/logical changes — only CSS and HTML presentation was modified.

### Design Philosophy

A Notion-inspired study tool that feels like a **premium notebook** — warm off-white
pages (`#faf9f7`) evoking paper texture, amber/copper accents (`#d97706`) that suggest
highlighter marks, and a sophisticated warm-dark sidebar for navigation. Clean spacing,
soft shadows, and refined typography (Inter) make it feel intentional, not cobbled together.

**Key principles:**
1. **Practical visibility** — messages must be easily readable, contrast ratios respected
2. **Modern minimalism** — Notion-style: lots of whitespace, soft shadows, clean hierarchy
3. **Warmth without distraction** — warm tones that feel inviting without being playful
4. **Subtle motion** — fade-in messages, smooth hover transitions, no gratuitous animation

### Color Palette

#### Main Area — Warm Paper

| Token | Hex | Usage |
|-------|-----|-------|
| `--bg` | `#faf9f7` | Page background — warm off-white, like premium paper |
| `--surface` | `#ffffff` | Card/surface backgrounds (assistant messages, input bar) |
| `--surface-hover` | `#f5f2ed` | Hover states on surfaces |
| `--input-bg` | `#f3f0ec` | Input/text field backgrounds |
| `--text` | `#1c1b1a` | Primary text — rich warm dark, never pure black |
| `--text-dim` | `#78716c` | Secondary text, labels, metadata |
| `--text-subtle` | `#a8a29e` | Placeholder text, captions |
| `--border` | `#e7e5e2` | Borders, dividers — warm gray |
| `--border-light` | `#f0eee9` | Lighter borders for subtle separation |

#### Sidebar — Warm Dark Charcoal

| Token | Hex | Usage |
|-------|-----|-------|
| `--sidebar-bg` | `#1c1a17` | Sidebar background — warm dark charcoal, not cold navy |
| `--sidebar-surface` | `#262320` | Surface elements within sidebar |
| `--sidebar-hover` | `#2f2c28` | Hover states in sidebar |
| `--sidebar-active` | `#38342f` | Active/selected state |
| `--sidebar-text` | `#d4cfc8` | Primary text in sidebar — warm light |
| `--sidebar-text-dim` | `#9d9690` | Muted text in sidebar |
| `--sidebar-border` | `#2d2a26` | Dividers in sidebar |

#### Accent — Amber/Copper

| Token | Hex | Usage |
|-------|-----|-------|
| `--accent` | `#d97706` | Primary accent — buttons, links, active indicators |
| `--accent-light` | `#fef3c7` | Light tint — user message bubbles, hover backgrounds |
| `--accent-hover` | `#b45309` | Hover state for accent elements |
| `--accent-text` | `#92400e` | Text on top of accent-light backgrounds |
| `--accent-gradient` | `linear-gradient(135deg, #d97706, #ea580c)` | Gradient for primary buttons |

#### Semantic

| Token | Hex | Usage |
|-------|-----|-------|
| `--success` / `--success-bg` | `#059669` / `#ecfdf5` | Indexed status, success states |
| `--warning` / `--warning-bg` | `#d97706` / `#fffbeb` | Not indexed, warnings |
| `--error` / `--error-bg` | `#dc2626` / `#fef2f2` | Errors, delete actions |

### Typography

| Property | Value |
|----------|-------|
| Font family | `Inter` (Google Fonts), with system fallback stack |
| Weights used | 400 (regular), 500 (medium), 600 (semibold), 700 (bold) |
| Body size | `0.9375rem` (15px) |
| Body line-height | `1.6` |
| Sidebar text | `0.875rem` |
| Sidebar caption | `0.75rem` |
| Code | Monospace, `#1c1b1a` on `#f5f2ed` |
| Sidebar code | `#d4cfc8` on `#262320` |

**Font source:** Google Fonts CDN with `font-display: swap` for fallback.

**Fallback stack:** `'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI',
Roboto, Oxygen, Ubuntu, Cantarell, sans-serif`

### Shadow System

| Level | Value | Where Used |
|-------|-------|------------|
| `--shadow-sm` | `0 1px 2px rgba(0,0,0,0.04)` | Messages, file cards, input bar default |
| `--shadow-md` | `0 2px 8px rgba(0,0,0,0.06)` | Input bar on focus, hovered cards |
| `--shadow-lg` | `0 4px 16px rgba(0,0,0,0.08)` | Modals, popovers |
| `--shadow-xl` | `0 8px 32px rgba(0,0,0,0.10)` | Overlays, panels |

### Border Radius

| Level | Value | Where Used |
|-------|-------|------------|
| `--radius-sm` | `6px` | Small buttons, rename inputs |
| `--radius-md` | `8px` | Regular buttons, sidebar inputs |
| `--radius-lg` | `12px` | Messages, cards, input bar, panels |
| `--radius-xl` | `16px` | Large containers, artifact panel |

### Motion & Animation

| Animation | Timing | Where Used |
|-----------|--------|------------|
| `messageIn` | 0.2s ease | Messages entering the chat (fade + translate) |
| `fadeIn` | 0.25-0.4s ease | Panels, empty states, suggested questions |
| Hover transitions | 150ms ease | All interactive elements |

### Component Breakdown

#### 1. Sidebar
- **Background:** Gradient `180deg` from `#1c1a17` to `#1f1d19`
- **Title:** `📚 Study RAG` with subtitle
- **Search bar:** `--sidebar-surface` bg, amber focus ring
- **New Chat button:** Amber gradient, subtle shadow, lift on hover
- **Subject expanders:** Color dot via `::before` pseudo-element using per-subject CSS variable
- **Session items:** Active state has amber left border; hover reveals rename/delete
- **Settings:** Clean expander, sliders with warm labels, Search All checkbox at top

#### 2. Top Bar — Glassmorphism
- `background: rgba(255, 255, 255, 0.80)` with `backdrop-filter: blur(12px)`
- Sticky positioning with subtle bottom border
- Subject name (bold) · session name (muted)
- Clear Chat button

#### 3. User Messages — Amber-Tinted Bubble
- `background: linear-gradient(135deg, #fef3c7, #fffbeb)`
- Left `3px` accent border in amber
- Floated right, `max-width: 78%`
- Subtle shadow and rounded corners

#### 4. Assistant Messages — White Card
- White background with `1px` warm border
- Subtle shadow for depth
- Hover reveals copy button

#### 5. Citation Pills
- Amber background with white text, rounded pills
- `user-select: none`

#### 6. Source Chunks
- Warm tint background, amber left border
- Expandable via `<details>`

#### 7. Input Bar
- White card with shadow, amber focus ring
- Send button uses amber gradient

#### 8. Suggested Questions
- Card-style Streamlit buttons with warm border
- Hover: amber border, warm background, slight lift

#### 9. Empty States
- Centered layout with large icon, heading, descriptive text

#### 10. Artifact Panel
- Warm background, amber-accent header separator
- Consistent action buttons

#### 11. File Manager
- File cards: icon, name, size, status pill, delete
- Status: green (indexed) / amber (not indexed)
- Progress bar: amber gradient fill

#### 12. Scrollbar
- Thin `6px` track, semi-transparent warm-thumb

### Responsive Design

| Breakpoint | Behavior |
|------------|----------|
| ≤ 768px | Sidebar max-width 260px; user bubbles float none; session name hidden; reduced padding |
| ≤ 480px | Tighter message padding, further reduced margins |

### What Changed from v1 (Migration Notes)

| v1 Element | v1 Style | v2 Style |
|------------|----------|----------|
| Sidebar bg | Cold navy `#1a1a2e` | Warm charcoal `#1c1a17` w/ gradient |
| Sidebar text | `#e0e0e0` | `#d4cfc8` (warmer) |
| Sidebar surface | No dedicated | `--sidebar-surface: #262320` |
| Sidebar active | Same-color darker | Distinct `#38342f` |
| Main bg | Sterile `#ffffff` | Warm paper `#faf9f7` |
| Accent | Indigo `#6366f1` | Amber `#d97706` |
| User messages | Barely visible `#f0f0ff` | Visible amber tint `#fef3c7` |
| Assistant messages | Plain text | White card + border + shadow |
| Citations | Indigo pills | Amber pills |
| Font | System default | Inter (Google Fonts) |
| Shadows | None | 4-tier shadow system |
| Animations | None | messageIn, fadeIn, transitions |
| Color dots | CSS existed, never rendered | Rendered via CSS variable |
| Top bar | Flat white bar | Glassmorphism w/ blur |
| Suggested Qs | Broken JS onclick | Proper Streamlit buttons |
| Search All toggle | Not exposed in UI | Checkbox in Settings |
| Clear Chat | No way to clear | Button in top bar |
| Scrollbar | Browser default | Custom warm-toned thin |

### Files Modified

| File | Change Type | Scope |
|------|-------------|-------|
| `src/ui/styles.py` | Full rewrite | All CSS replaced with Design System v2 |
| `src/ui/sidebar.py` | Moderate | Color dots, Search All toggle, refined meta row |
| `src/ui/chat.py` | Moderate | Clear Chat btn, glass top bar, suggested Qs fix, msg class updates |
| `src/ui/app.py` | Minor | Empty state styling, `pending_question` session state |
| `src/ui/artifacts_panel.py` | Minor | Refined CSS classes for amber styling |
| `src/ui/file_manager.py` | Minor | File cards, status pills, upload modal styling |
| `PLAN.md` | Documentation | This section — Design System v2 documented |

### Design Rationale — Why Amber?

Amber/copper (`#d97706`) was chosen over the original indigo (`#6366f1`) because:

1. **Study context** — Amber evokes highlighters, warm lighting, paper notepads.
   Indigo feels corporate/SaaS — more "dashboard" than "study tool."
2. **Readability** — Amber on off-white has better contrast than indigo on white
   for user messages. The original `#f0f0ff` on `#ffffff` was barely visible.
3. **Emotional tone** — Warm tones feel inviting for extended study sessions.
   Cool tones (navy + indigo) feel clinical.
4. **Modern trend** — 2025-2026 design favors warm neutrals (cream, beige, warm gray)
   over cold blues for content-focused apps (Notion, Craft, Linear).
5. **Accessibility** — Amber `#d97706` passes WCAG AA on white backgrounds.

---

## Changelog

| Date | Change |
|------|--------|
| 2026-06-23 | Initial plan created |
| 2026-06-23 | Restructured to `src/` layout for maintainability |
| 2026-06-23 | Added `models.py`, `exceptions.py` for type safety |
| 2026-06-23 | Split loaders by format (pdf_loader, pptx_loader, scanner) |
| 2026-06-23 | Completed Phase 0–2: setup, config, document loading |
| 2026-06-23 | Added todo.md for progress tracking |
| 2026-06-23 | Bug review on Phases 0–2: found & fixed 5 bugs (see Bugs Fixed section) |
| 2026-06-23 | Completed Phase 3: embeddings.py + vector_store.py |
| 2026-06-23 | Completed Phase 4: rag_chain.py — prompt building, DeepSeek streaming, get_answer() |
| 2026-06-23 | Completed Phase 5: chat_store.py, artifact_store.py — persistence layer |
| 2026-06-23 | Completed Phase 6: prompts.py, parser.py, generator.py — artifact system |
| 2026-06-23 | Phase 0–6 cross-phase review: found & fixed 4 bugs (1 critical, 2 medium, 1 low) |
| 2026-06-23 | Completed Phase 7: styles.py, app.py, sidebar.py — UI setup |
| 2026-06-23 | Fixed sidebar CSS — all selectors updated for Streamlit 1.58.0 (expander, caption, slider, alert, markdown) |
| 2026-06-25 | Completed Phase 8: chat.py — chat UI with messages, streaming, citations, input bar |
| 2026-06-25 | Completed Phase 9: file_manager.py — upload modal, file list with delete, rebuild index with progress bar |
| 2026-06-25 | Completed Phase 10: artifacts_panel.py — slide-in panel, streaming, copy/download, sidebar artifact list |
| 2026-06-25 | Doc audit: corrected all line counts (~2256→~2665), removed phantom settings.py, updated file tree, run commands |
| 2026-06-26 | **Design System v2 "Warm Academia"** — complete UI redesign: new color palette (amber/copper on warm paper), Inter font, glassmorphism top bar, card-style messages, animated transitions, responsive layout, subject color dots, Search All toggle, Clear Chat button, fixed suggested questions, custom scrollbar |
| 2026-06-26 | Bug fix: CSS split into BASE + ENHANCED blocks to avoid Streamlit sanitizer rejecting complex selectors (removed all `:has()` from base block) |
| 2026-06-26 | Bug fix: `.streamlit/config.toml` updated to v2 colors — `primaryColor=#d97706`, `backgroundColor=#faf9f7`, `textColor=#1c1b1a` — old theme was overriding new CSS |
| 2026-06-26 | Bug fix: User message bubble `#fef3c7` was invisible against `#faf9f7` bg (1.1:1 contrast). Changed to white card with 4px amber left border. |
| 2026-06-26 | Bug fix: Artifact copy button had broken inline `:hover` concatenation causing visible CSS text. Replaced with CSS class `.artifact-copy-btn`. |
| 2026-06-26 | Bug fix: Subject color dots wrapper div couldn't contain Streamlit expander elements. Dot now renders inside expander body only. |
| 2026-06-26 | Bug fix: Chat container wrapper div couldn't contain Streamlit elements. Replaced with `st.columns([1,6,1])` centering approach. |
| 2026-06-26 | Bug fix: Scrollbar thumb increased from 19% to 50% opacity for visibility on light backgrounds. |
| 2026-06-26 | **Phase 11 Complete** — Enhanced responsive CSS: sidebar collapse at 768px/480px, hamburger menu prominence, artifact panel mobile layout, glassmorphism top bar responsive padding |
| 2026-06-26 | **Phase 12 Complete** — 13 integration tests passed (all modules). Fixed parser bug: `parse_slash_command` returned `None` instead of `(None, "")` causing crash on unknown commands. App launches cleanly. |
| 2026-06-26 | **CSS injection crisis fix** — `st.markdown(unsafe_allow_html=True)` fails on `<style>` blocks in Streamlit 1.58.0. Tried `st.html()` (renders as visible text), then `st.markdown` with separated `<link>` tags (still broken). Final fix: custom `css_injector.py` using `st.components.v1.html()` with JavaScript to inject CSS into parent document `<head>`. |
| 2026-06-26 | **Inline styles migration** — Streamlit's HTML sanitizer strips `class` attributes from `st.markdown()` content. All 36 `class=` references across 5 files (chat.py, sidebar.py, app.py, file_manager.py, artifacts_panel.py) converted to inline `style=` attributes. |
| 2026-06-26 | Added Material Icons font to FONT_LINK (fixes "keyboard_double_arrow_down" text rendering) |
| 2026-06-26 | Improved error handling: `rag_chain.py` now shows clear message when no FAISS index exists ("Build Index first") |
| 2026-06-26 | Fixed sidebar title visibility: `color:#f0ebe5 !important` to override Streamlit CSS |
| 2026-06-26 | Added "← Back to Chat" button in file manager (was missing — user couldn't return to chat) |
| 2026-06-26 | Fixed sidebar alignment: consistent spacing, search input styling, button/expander padding, removed duplicate CSS rules |
| 2026-06-26 | Fixed rename/delete icon button alignment: `use_container_width=True` + compact CSS for buttons in columns |

---

## CSS Injection Bug Fixes (2026-06-26)

| # | Severity | File | Issue | Fix |
|---|----------|------|-------|-----|
| 1 | CRITICAL | `app.py`, `styles.py` | `st.markdown(unsafe_allow_html=True)` renders `<style>` blocks as visible text in Streamlit 1.58.0 | Created `css_injector.py` using `st.components.v1.html()` with JavaScript to inject CSS into parent document `<head>` |
| 2 | CRITICAL | 5 UI files | Streamlit's HTML sanitizer strips `class` attributes from `st.markdown()` content | Converted all 36 `class=` references to inline `style=` attributes |
| 3 | HIGH | `styles.py` | `<link>` tag concatenated with `<style>` block — sanitizer rejects `<link>`, breaks entire block | Separated FONT_LINK into its own `inject_css()` call |
| 4 | HIGH | `styles.py` | Material Icons font not loaded — icons rendered as text | Added Material Symbols Outlined to FONT_LINK |
| 5 | HIGH | `rag_chain.py` | `delta.content` truthiness check fails when content is `None` | Changed to `is not None` check |
| 6 | HIGH | `rag_chain.py` | No clear error when FAISS index missing | Added `IndexNotFoundError` catch with helpful message |
| 7 | MEDIUM | `sidebar.py` | Title color overridden by Streamlit CSS | Added `!important` to inline style |
| 8 | MEDIUM | `file_manager.py` | No way to return from Manage Files to chat | Added "← Back to Chat" button |
| 9 | MEDIUM | `styles.py`, `sidebar.py` | Sidebar elements had inconsistent spacing | Added consistent gap/padding rules, removed duplicates |
| 10 | LOW | `sidebar.py`, `styles.py` | Icon buttons overflowed their columns | Added `use_container_width=True` + compact CSS |

---

## Bugs Fixed (Phases 0–2 Review)

| # | Severity | File | Issue | Fix |
|---|----------|------|-------|-----|
| 1 | HIGH | `src/loaders/__init__.py:51,70` | Raises `ValueError` instead of `DocumentLoadError` for unsupported file types | Changed to `DocumentLoadError` + added import |
| 2 | HIGH | `src/models.py` | Missing `SourceChunk.from_dict()` and `to_dict()` — breaks chat history deserialization | Added `from_dict()` and `to_dict()` classmethods; updated `ChatMessage` to use them |
| 3 | MEDIUM | `src/config.py:77` | `hash()` is non-deterministic across Python processes — subject colors change on restart | Replaced with `hashlib.md5()` for deterministic color assignment |
| 4 | MEDIUM | `src/loaders/__init__.py:112-114` | Silent file load failures — only logged per-file, no summary | Added `failed_files` list + warning summary with count and names |
| 5 | LOW | `.gitignore:38` | `chat_history/*` inconsistent with `data/*/` pattern | Changed to `chat_history/*/` |

---

## Phase 4 Review Notes

| # | Severity | File | Issue | Status |
|---|----------|------|-------|--------|
| 1 | LOW | `src/retrieval/rag_chain.py:110-112` | `_get_client()` creates a new `OpenAI` client per call — should be a singleton for efficiency | Noted (not a bug, minor optimization) |
| 2 | LOW | `PLAN.md:381` | File Responsibilities table said `rag_chain.py` was "~100 lines / Pending" — actual is 208 lines / Done | Fixed |

---

## Phase 0–6 Cross-Phase Review

| # | Severity | File | Issue | Fix |
|---|----------|------|-------|-----|
| 1 | CRITICAL | `src/artifacts/generator.py:102-103` | `Artifact(id="", ...)` — empty ID creates file `artifacts/<subject>/.md` (missing filename) | Added `import uuid`, changed to `id=str(uuid.uuid4())` |
| 2 | MEDIUM | `PLAN.md:483-517` | Chat History JSON Schema showed `file`/`snippet` — actual code uses `source`/`content`/`page`/`score` | Updated schema to match actual `SourceChunk.to_dict()` output |
| 3 | MEDIUM | `src/retrieval/rag_chain.py:110` | `_get_client()` (private) imported externally by `generator.py` | Renamed to `get_client()` (public) |
| 4 | LOW | `src/retrieval/rag_chain.py:110-112` | No validation that `DEEPSEEK_API_KEY` is configured | Added check for empty/placeholder key with clear error message |

**Note:** Bug 4 from initial analysis (`get_files` not in `loaders.__all__`) was a false positive — already present.

