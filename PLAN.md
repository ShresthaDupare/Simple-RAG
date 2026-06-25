# Study RAG Assistant — Master Plan

> **This is the living document for the project.** All design decisions, features, and changes are tracked here. Update this file whenever features are added, removed, or modified.

**Last updated:** 2026-06-23 (Phase 7 complete)

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

## UI Design

### Visual Style: ChatGPT + Claude Hybrid

**Color Palette:**

| Element | Color |
|---------|-------|
| Background | `#ffffff` |
| Sidebar bg | `#1a1a2e` (dark navy) |
| Sidebar text | `#e0e0e0` |
| Sidebar hover | `#2a2a4a` |
| Sidebar active | `#3a3a5a` |
| Primary accent | `#6366f1` (indigo) |
| User message bg | `#f0f0ff` (light indigo tint) |
| Assistant message | `#ffffff` (plain text, no bubble) |
| Citation pills | `#6366f1` on `#f0f0ff` |
| Input bg | `#f7f7f8` |
| Input border | `#e5e5e5` |
| Send button | `#6366f1` |
| Text | `#1a1a2e` |
| Subtle text | `#888888` |

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
│       ├── sidebar.py          # Sidebar rendering
│       ├── chat.py             # Chat display + input
│       ├── artifacts_panel.py  # Artifact slide-in panel
│       ├── file_manager.py     # Upload, list, delete files
│       ├── settings.py         # Settings sliders
│       └── styles.py           # All CSS in one place
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
| `src/retrieval/embeddings.py` | Sentence-transformer wrapper | ~40 | Done |
| `src/retrieval/vector_store.py` | FAISS create/load/search/search-all | ~100 | Done |
| `src/retrieval/rag_chain.py` | Prompt building + DeepSeek streaming | ~213 | Done |
| `src/storage/chat_store.py` | JSON CRUD for sessions | ~100 | Done |
| `src/storage/artifact_store.py` | Artifact file management | ~90 | Done |
| `src/artifacts/prompts.py` | All artifact prompt templates | ~45 | Done |
| `src/artifacts/parser.py` | Slash command parsing | ~95 | Done |
| `src/artifacts/generator.py` | Streaming artifact generation | ~120 | Done |
| `src/ui/styles.py` | All CSS in one place | ~200 | Done |
| `src/ui/app.py` | Main entry, session state, routing | ~100 | Done |
| `src/ui/sidebar.py` | Sidebar rendering | ~150 | Done |
| `src/ui/chat.py` | Chat display + input | ~200 | Pending |
| `src/ui/artifacts_panel.py` | Artifact slide-in panel | ~100 | Pending |
| `src/ui/file_manager.py` | Upload, list, delete files | ~80 | Pending |
| `src/ui/settings.py` | Settings sliders | ~60 | Pending |

**Total: ~2096 lines across 22 files.**

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

### Phase 8: Chat UI (Pending)
- `src/ui/chat.py` — messages, input, streaming, citations

### Phase 9: File Manager UI (Pending)
- `src/ui/file_manager.py` — upload, list, delete, rebuild index

### Phase 10: Artifacts UI (Pending)
- `src/ui/artifacts_panel.py` — slide-in panel, slash commands, autocomplete

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
streamlit run src/ui/app.py
```

---

## Pre-requisites

1. **DeepSeek API key** — paste into `.env` as `DEEPSEEK_API_KEY=sk-...`
2. **Study files** — create subject folders in `data/` and copy PDFs/PPTX there
3. **Python 3.9+** installed

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

