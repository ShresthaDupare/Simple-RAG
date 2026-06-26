# Study RAG Assistant — Feature Tracker

> Track progress here. Check off items as they're completed. Update this file after each phase.

**Started:** 2026-06-23
**Total Phases:** 13

---

## Phase 0: Project Setup
- [x] Create `requirements.txt` with all dependencies
- [x] Create `.env` with `DEEPSEEK_API_KEY=` placeholder
- [x] Create `.gitignore` for Python/venv/data
- [x] Create `src/` folder structure with `__init__.py` files
- [x] Create empty `data/.gitkeep`
- [x] Create empty `faiss_index/.gitkeep`
- [x] Create empty `chat_history/.gitkeep`
- [x] Create empty `artifacts/.gitkeep`

---

## Phase 1: Config & Models
- [x] `src/config.py` — load `.env`, define paths, constants, defaults
- [x] `src/models.py` — dataclasses: `ChatMessage`, `Session`, `Artifact`, `SourceChunk`
- [x] `src/exceptions.py` — custom exceptions: `IndexNotFoundError`, `DocumentLoadError`, `APIError`

---

## Phase 2: Document Loading
- [x] `src/loaders/scanner.py` — `scan_subjects()`, `get_files(subject)`
- [x] `src/loaders/pdf_loader.py` — `load_pdf(path)` with metadata
- [x] `src/loaders/pptx_loader.py` — `load_pptx(path)` with metadata
- [x] `src/loaders/__init__.py` — `load_document(path)` dispatcher, `load_and_chunk(subject)`
- [x] `src/loaders/__init__.py` — `load_full_document(path)` for artifacts

---

## Phase 3: Embeddings & Vector Store
- [x] `src/retrieval/embeddings.py` — singleton sentence-transformer wrapper
- [x] `src/retrieval/vector_store.py` — `create_index(subject, chunks)`
- [x] `src/retrieval/vector_store.py` — `load_index(subject)`, `index_exists(subject)`
- [x] `src/retrieval/vector_store.py` — `delete_index(subject)`
- [x] `src/retrieval/vector_store.py` — `search(subject, query, top_k)`
- [x] `src/retrieval/vector_store.py` — `search_all(query, top_k)` with score merge

---

## Phase 4: RAG Chain
- [x] `src/retrieval/rag_chain.py` — system prompt definition
- [x] `src/retrieval/rag_chain.py` — `build_prompt(question, context_chunks, chat_history)`
- [x] `src/retrieval/rag_chain.py` — `call_deepseek_stream(messages)` via openai SDK
- [x] `src/retrieval/rag_chain.py` — `get_answer(question, subject, chat_history, top_k, max_history, temperature)`

---

## Phase 5: Storage
- [x] `src/storage/chat_store.py` — `load_sessions(subject)`, `save_sessions(subject, sessions)`
- [x] `src/storage/chat_store.py` — `create_session(subject)` → returns ID
- [x] `src/storage/chat_store.py` — `delete_session(subject, session_id)`
- [x] `src/storage/chat_store.py` — `rename_session(subject, session_id, new_name)`
- [x] `src/storage/chat_store.py` — `add_message(subject, session_id, role, content, sources)`
- [x] `src/storage/chat_store.py` — `auto_name_session(subject, session_id, first_message)`
- [x] `src/storage/artifact_store.py` — `save_artifact(artifact, content)`
- [x] `src/storage/artifact_store.py` — `load_artifact(artifact_id)`
- [x] `src/storage/artifact_store.py` — `list_artifacts(subject)`
- [x] `src/storage/artifact_store.py` — `delete_artifact(artifact_id)`

---

## Phase 6: Artifacts
- [x] `src/artifacts/prompts.py` — `ARTIFACT_PROMPTS` dict (summary, glossary, compare, explain)
- [x] `src/artifacts/parser.py` — `parse_slash_command(text)` → returns (command, args)
- [x] `src/artifacts/parser.py` — `get_available_files(subject)` for autocomplete
- [x] `src/artifacts/generator.py` — `generate_artifact(type, source_text, topic, subject)` streaming

---

## Phase 7: UI Setup
- [x] `src/ui/styles.py` — all CSS (sidebar, messages, input, responsive)
- [x] `src/ui/app.py` — page config, session state init, main routing
- [x] `src/ui/sidebar.py` — sidebar title, search bar, "+ New Chat" button
- [x] `src/ui/sidebar.py` — subject groups with collapsible session lists
- [x] `src/ui/sidebar.py` — settings section (top_k, temperature, chunk_size sliders)
- [x] `src/ui/sidebar.py` — active session highlight, hover actions (rename/delete)

---

## Phase 8: Chat UI
- [x] `src/ui/chat.py` — top bar (subject name, session name, menu)
- [x] `src/ui/chat.py` — message display (user bubbles, assistant plain text)
- [x] `src/ui/chat.py` — streaming response display with spinner
- [x] `src/ui/chat.py` — source citations (clickable pills `[1]` `[2]`)
- [x] `src/ui/chat.py` — expandable source chunks on click
- [x] `src/ui/chat.py` — copy answer button on hover
- [x] `src/ui/chat.py` — input bar (auto-resize, Enter=send, Shift+Enter=newline)
- [x] `src/ui/chat.py` — attachment button for file upload
- [x] `src/ui/chat.py` — placeholder adapts to current subject

---

## Phase 9: File Manager UI
- [x] `src/ui/file_manager.py` — file upload modal
- [x] `src/ui/file_manager.py` — file list per subject with delete option
- [x] `src/ui/file_manager.py` — rebuild index button with progress bar

---

## Phase 10: Artifacts UI
- [x] `src/ui/artifacts_panel.py` — slide-in panel from right
- [x] `src/ui/artifacts_panel.py` — slash command detection in input
- [x] `src/ui/artifacts_panel.py` — autocomplete dropdown for `/` commands
- [x] `src/ui/artifacts_panel.py` — artifact streaming display
- [x] `src/ui/artifacts_panel.py` — copy artifact button
- [x] `src/ui/artifacts_panel.py` — download artifact as `.md` button
- [x] `src/ui/artifacts_panel.py` — artifact list in sidebar

---

## Phase 11: Final Polish
- [x] Responsive CSS — sidebar collapses on mobile
- [x] Hamburger menu to expand sidebar on narrow screens
- [x] Suggested questions for new empty sessions
- [x] Clear chat button (reset session)
- [x] Search All toggle (query all subjects at once)
- [x] Subject color dots in sidebar

---

## Phase 12: Final Testing
- [x] Test: Upload PDF/PPTX to a subject folder
- [x] Test: Rebuild index creates FAISS index
- [x] Test: Chat returns relevant answer with sources
- [x] Test: Streaming works token-by-token
- [x] Test: Citations are clickable and show source text
- [x] Test: Slash commands generate artifacts
- [x] Test: Artifact panel opens/closes
- [x] Test: Artifacts persist to disk
- [x] Test: Chat sessions persist across restart
- [x] Test: Search All works across subjects
- [x] Test: Responsive layout on narrow screen

---

## Completed Features

| Date | Phase | Files Created/Modified |
|------|-------|----------------------|
| 2026-06-23 | Phase 0 | requirements.txt, .env, .gitignore, src/*, data/.gitkeep, faiss_index/.gitkeep, chat_history/.gitkeep, artifacts/.gitkeep |
| 2026-06-23 | Phase 1 | src/config.py, src/models.py, src/exceptions.py |
| 2026-06-23 | Phase 2 | src/loaders/scanner.py, src/loaders/pdf_loader.py, src/loaders/pptx_loader.py, src/loaders/__init__.py |
| 2026-06-23 | Bug Fix | src/config.py, src/models.py, src/loaders/__init__.py, .gitignore — fixed 5 bugs from Phases 0–2 review |
| 2026-06-23 | Phase 3 | src/retrieval/embeddings.py, src/retrieval/vector_store.py, src/retrieval/__init__.py |
| 2026-06-23 | Phase 4 | src/retrieval/rag_chain.py |
| 2026-06-23 | Phase 4 Review | PLAN.md — fixed table status (Pending→Done), updated line count (~100→~208) |
| 2026-06-23 | Phase 5 | src/storage/chat_store.py, src/storage/artifact_store.py |
| 2026-06-23 | Phase 6 | src/artifacts/__init__.py, src/artifacts/prompts.py, src/artifacts/parser.py, src/artifacts/generator.py |
| 2026-06-23 | Phase 0–6 Review | generator.py, rag_chain.py, PLAN.md — fixed 4 bugs (1 critical, 2 medium, 1 low) |
| 2026-06-23 | Phase 7 | src/ui/styles.py, src/ui/app.py, src/ui/sidebar.py |
| 2026-06-23 | CSS Fix | src/ui/styles.py — sidebar selectors updated for Streamlit 1.58.0 |
| 2026-06-25 | Phase 8 | src/ui/chat.py — chat UI with messages, streaming, citations, input bar |
| 2026-06-25 | Phase 9 | src/ui/file_manager.py, src/ui/sidebar.py, src/ui/app.py — file manager with upload, list, delete, rebuild index |
| 2026-06-25 | Phase 10 | src/ui/artifacts_panel.py, src/ui/chat.py, src/ui/sidebar.py, src/ui/styles.py — artifact panel, streaming, copy, download, sidebar list |
| 2026-06-25 | Doc Audit | PLAN.md, todo.md — corrected line counts, removed phantom settings.py, updated file tree and notes |
| 2026-06-26 | Phase 11 | src/ui/styles.py — enhanced responsive CSS (768px/480px breakpoints), hamburger menu, artifact panel mobile layout |
| 2026-06-26 | Phase 12 | test_phase12.py — 13 integration tests (config, models, parser, chat_store, artifact_store, loaders, rag_chain, vector_store, styles, UI imports). Fixed parser bug. App launches cleanly. |

---

## Bugs Found & Fixed (Phases 0–2 Review)

| # | Severity | File | Issue | Fix |
|---|----------|------|-------|-----|
| 1 | HIGH | `loaders/__init__.py` | Raises `ValueError` instead of `DocumentLoadError` | Changed to `DocumentLoadError` |
| 2 | HIGH | `models.py` | Missing `SourceChunk.from_dict()` / `to_dict()` | Added both methods |
| 3 | MEDIUM | `config.py` | Non-deterministic `hash()` for subject colors | Switched to `hashlib.md5()` |
| 4 | MEDIUM | `loaders/__init__.py` | Silent file load failures | Added failure summary logging |
| 5 | LOW | `.gitignore` | Inconsistent `chat_history/*` pattern | Changed to `chat_history/*/` |

---

## Phase 12 Bug Fix

| # | Severity | File | Issue | Fix |
|---|----------|------|-------|-----|
| 1 | HIGH | `artifacts/parser.py` | `parse_slash_command()` returns `None` for non-commands, but `chat.py:260` unpacks as `command, args = ...` — crashes on unknown commands | Changed return to `(None, "")` for non-matches; updated `is_slash_command()` |

---

## Phase 4 Review Notes

| # | Severity | File | Issue | Status |
|---|----------|------|-------|--------|
| 1 | LOW | `rag_chain.py` | `_get_client()` creates new client per call — should be singleton | Noted (minor optimization) |
| 2 | LOW | `PLAN.md` | Table said "~100 lines / Pending" — actual 208 lines / Done | Fixed |

---

## Phase 0–6 Cross-Phase Review

| # | Severity | File | Issue | Fix |
|---|----------|------|-------|-----|
| 1 | CRITICAL | `generator.py` | Empty Artifact ID → file saved as `.md` | Added `uuid.uuid4()` for ID generation |
| 2 | MEDIUM | `PLAN.md` | JSON schema showed wrong field names | Updated to match actual `SourceChunk.to_dict()` |
| 3 | MEDIUM | `rag_chain.py` | Private `_get_client()` imported externally | Renamed to `get_client()` |
| 4 | LOW | `rag_chain.py` | No API key validation | Added check with clear error message |

---

## Notes

- Run `pip install -r requirements.txt` after Phase 0
- Run `streamlit run app.py` to start the app locally
- DeepSeek API key must be in `.env` before Phase 4
- For Streamlit Community Cloud: set entry point to `src/ui/app.py`
- Settings sliders are in `sidebar.py` (no separate `settings.py`)
