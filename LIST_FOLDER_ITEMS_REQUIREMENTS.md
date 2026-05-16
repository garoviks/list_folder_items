# List Folder Items — Requirements

**Current version: v1.0**

## Overview

List Folder Items is a dual-pane folder browser web app. It displays the contents of two directories side by side, with navigation, sorting, and filtering. View-only — no file operations.

| Item | Value |
|------|-------|
| Default left folder | `/home/nesha/Downloads/comics_download/` |
| Default right folder | `/mnt/extramedia/Comics/` |
| Server | `http://localhost:8200` |

---

## Functional Requirements

### FR1: Dual-Pane Display

- Two panes displayed side by side, equal width
- Each pane independently shows the contents of one directory
- Default paths loaded on startup without user input

### FR2: Directory Listing

- List direct children only (top-level, no recursion)
- Show both files and folders mixed in the same list
- For each item display:

| Column | Files | Folders |
|--------|-------|---------|
| Name | filename without extension | folder name |
| Ext | file extension | *(empty)* |
| Items | *(empty)* | count of direct children |
| Size | human-readable (MiB/KiB/B) | *(empty)* |
| Modified | date and time | date and time |

- `..` entry pinned at top of each pane (when not at root) for parent navigation
- Inaccessible subdirectory item count shown as `?`

### FR3: Navigation

- **Double-click** a folder or `..` to navigate into it
- Each pane maintains independent navigation history
- **◀ Back** button: return to previous directory in that pane
- **▶ Forward** button: go forward after going back
- Back/Forward buttons disabled when history is empty
- Current path displayed in toolbar above each pane

### FR4: Sorting

- Click any column header to sort by that column
- First click: ascending (↑); second click on same column: descending (↓)
- Sort indicator shown in active column header
- Sort persists within a pane until changed
- Sort keys: Name/Ext → alphabetic; Items/Size → numeric; Modified → chronological
- `..` row always stays pinned at top regardless of sort

### FR5: Filtering

- Filter input at the bottom of each pane
- Case-insensitive substring match on the Name column
- Applied instantly as the user types (no button needed)
- Filter cleared automatically when navigating to a new folder

### FR6: Security

- Server only serves paths within the two allowed roots
- Requests outside allowed roots return HTTP 403

---

## Non-Functional Requirements

### Performance
- Directory listing response should feel instant for directories up to ~10,000 items
- Item count for subdirectories fetched via `os.scandir` — no recursion

### Usability
- Dark theme consistent with cp_downloads2comics
- Monospace font for numeric columns (size, items, modified)
- Hover highlight on rows

### Simplicity
- No external dependencies — Python stdlib only
- Single HTML file, single Python server file

---

## Out of Scope (v1.0)

- File copy, move, delete, or rename
- Opening files or launching applications
- Recursive folder scanning
- Bookmarks or saved paths
- Multi-tab or multi-window
- Search across subdirectories
- Drag and drop

---

## Constraints

- **Python 3.8+** — standard library only
- **Local filesystem** — mounted paths only
- **Browser**: Modern ES6 (Chrome, Firefox, Edge)

---

**Version**: v1.0
**Last Updated**: 2026-05-16
