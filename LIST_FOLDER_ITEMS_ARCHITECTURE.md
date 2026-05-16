# List Folder Items — Architecture

**Current version: v1.1**

## System Overview

A dual-pane folder browser web app. The browser UI requests directory listings from a minimal Python HTTP server; no state is stored server-side between requests.

```
┌─────────────────────────────────┐
│   User Browser                  │
│ (list_folder_items.html)        │
│                                 │
│  • Two-pane layout              │
│  • Navigation history per pane  │
│  • Sortable columns             │
│  • Filter bars                  │
└──────────┬──────────────────────┘
           │ HTTP
           ▼
┌──────────────────────────────────┐
│ list_folder_items_server.py      │
│ (port 8200)                      │
│                                  │
│  GET  /          → HTML          │
│  GET  /api/list  → JSON          │
└──────────────────────────────────┘
           │
           ▼
      Filesystem
  /home/nesha/Downloads/
  comics_download/        ← default left
  /mnt/extramedia/Comics/ ← default right
```

---

## Technology Stack

### Backend
- **Language**: Python 3.8+
- **Web Framework**: `http.server.BaseHTTPRequestHandler` (stdlib)
- **File Operations**: `os.scandir`, `pathlib`, `os.stat`

### Frontend
- **Markup**: HTML5
- **Styling**: CSS3 — dark theme matching cp_downloads2comics
- **Scripting**: Vanilla JavaScript ES6+ (no frameworks)
- **Protocol**: HTTP/1.1

---

## Component Architecture

### 1. `list_folder_items_server.py` — HTTP Server

**Port:** 8200

**Allowed roots** (security boundary):
```python
ALLOWED_ROOTS = [
    Path("/home/nesha/Downloads/comics_download/").resolve(),
    Path("/mnt/extramedia/Comics").resolve(),
]
```
Any request for a path outside these roots returns HTTP 403.

#### Endpoints

**`GET /`**
- Reads and serves `list_folder_items.html` from the same directory

**`GET /api/list?path=/some/path`**
- Validates path is within ALLOWED_ROOTS
- Calls `list_dir(path)` → returns JSON

**`list_dir(path)` — core function:**
```python
{
  "path": "/mnt/extramedia/Comics",
  "parent": "/mnt/extramedia",   # None if at root
  "items": [
    {
      "name":        "Saga (2012)",
      "ext":         "",
      "is_dir":      true,
      "items_count": 54,          # direct children count
      "size_bytes":  null,
      "size":        null,
      "mtime":       1710506523.4, # unix timestamp for sort
      "modified":    "15/03/24 02:22 PM"
    },
    {
      "name":        "Feral 021",
      "ext":         "cbr",
      "is_dir":      false,
      "items_count": null,
      "size_bytes":  163182592,
      "size":        "155.6 MiB",
      "mtime":       1745516274.1,
      "modified":    "24/04/25 05:57 PM"
    }
  ]
}
```

**Size formatting:**
```python
≥ 1 MiB → "X.X MiB"
≥ 1 KiB → "X.X KiB"
< 1 KiB → "N B"
```

**Date formatting:** `dd/mm/yy HH:MM AM/PM`

**Sorting:** case-insensitive by name (server-side initial sort only; client re-sorts on column click)

---

### 2. `list_folder_items.html` — Web UI

#### State (JS)

```javascript
const state = {
  left: {
    path: '/home/nesha/Downloads/comics_download/',
    data: [],          // items array from last /api/list response
    parent: null,      // parent path or null
    sort: { col: 'name', dir: 'asc' },
    backStack: [],     // navigation history (back)
    fwdStack: [],      // navigation history (forward)
  },
  right: { /* same shape */ },
};
```

#### Layout

```
┌─────────────────────────────────────────────────────┐
│  List Folder Items                           header  │
├──────────────────────┬──────────────────────────────┤
│ ◀ ▶ /path/left/     │ ◀ ▶ /path/right/             │ ← toolbar
├──────────────────────┼──────────────────────────────┤
│ Name │Ext│Items│Size│Modified  (×2)                 │ ← sticky thead
│ ..                   │ ..                            │
│ folder/   54         │ folder/  12                  │ ← dblclick navigates
│ file.cbr  155.6 MiB  │ file.csv 549 B               │
│  ⋮                   │  ⋮                            │
├──────────────────────┼──────────────────────────────┤
│ Filter: [__________] │ Filter: [__________]          │ ← filter bar
└──────────────────────┴──────────────────────────────┘
```

#### Key Functions

**Navigation:**
- `navigate(side, path)` — push current to backStack, clear fwdStack, load
- `goBack(side)` — pop backStack → push to fwdStack → load
- `goForward(side)` — pop fwdStack → push to backStack → load
- `_loadPane(side, path)` — fetch `/api/list`, update state, call renderPane
- `updateNavButtons(side)` — disable ◀/▶ when stacks are empty

**Rendering:**
- `renderPane(side)` — applies current filter + sort, builds table HTML, injects into DOM
- After injection: attaches `dblclick` listeners to `tr[data-path]` elements via `querySelectorAll`

> **Why data-path + JS listeners (not inline onclick):**
> `JSON.stringify(path)` produces double-quoted strings that break HTML attribute parsing when embedded in `ondblclick="..."`. Using `data-path` attributes avoids this entirely.

**Sorting:**
- `setSort(side, col)` — toggle dir if same col, else set new col + asc; re-renders
- `sortItems(items, col, dir)` — sort by: name/ext (string), items/size (numeric via `items_count`/`size_bytes`), modified (numeric via `mtime`)

**Filtering:**
- `filterPane(side)` — reads filter input, calls `renderPane(side)`
- Filter applied client-side on `state[side].data` — no server roundtrip

**Preview overlay:**
- `hoveredRow` — global; tracks the last hovered or clicked `tr[data-path]` row
- `openPreview(tr)` — fetches `/api/list?path=tr.dataset.path`, positions overlay, renders contents
- `closePreview()` — hides overlay
- `positionOverlay(overlay, tr)` — right of row preferred; falls back to left; clamps to viewport
- `renderPreviewBody(items)` — folders-first table inside overlay (Name/Ext/Size)
- Space keydown → `openPreview(hoveredRow)`; Esc or click outside → `closePreview()`
- Hover and single-click both set `hoveredRow` — so Space works either way

**Utilities:**
- `basename(path)` — last segment of a path string
- `esc(s)` — HTML-escapes strings before inserting into innerHTML
- `scrollToFolder(side, name)` — scroll to and flash-highlight a folder row after back-navigation

#### Column Definitions

| Column | Width | File value | Folder value | Sort key |
|--------|-------|------------|--------------|----------|
| Name | auto | stem (no ext) | folder name | `name` (string) |
| Ext | 52px | extension | *(empty)* | `ext` (string) |
| Items | 62px | *(empty)* | direct child count | `items_count` (numeric) |
| Size | 90px | human-readable | *(empty)* | `size_bytes` (numeric) |
| Modified | 140px | date+time | date+time | `mtime` (numeric) |

---

## Security

- All `path` parameters validated against `ALLOWED_ROOTS` before `os.scandir`
- `PermissionError` on item count (inaccessible subdirs) → `items_count = null` displayed as `?`
- No file writes, deletes, or moves — read-only server

---

**Version**: v1.1
**Last Updated**: 2026-05-16
**Server**: `list_folder_items_server.py` (port 8200)
**UI**: `list_folder_items.html`
