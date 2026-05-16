# List Folder Items — User Guide

**Current version: v1.1**

---

## Quick Start

### 1. Start the Server

```bash
cd /home/nesha/scripts/list_folder_items
python3 list_folder_items_server.py
```

### 2. Open in Browser

```
http://localhost:8200
```

Both panes load automatically with the default folders.

---

## Interface Overview

```
┌─────────────────────────────────────────────────────┐
│  List Folder Items                                  │
├──────────────────────┬──────────────────────────────┤
│ ◀ ▶ /left/path/     │ ◀ ▶ /right/path/             │
├──────────────────────┼──────────────────────────────┤
│ Name │Ext│Items│Size│Modified │ Name│Ext│Items│...  │
│ ..                   │ ..                            │
│ 📁 Saga (2012)  54   │ 📁 Feral (2024)  12          │
│ 📄 file    cbr  ...  │ 📄 loose cbr 67.7 MiB        │
├──────────────────────┼──────────────────────────────┤
│ Filter: [__________] │ Filter: [__________]          │
└──────────────────────┴──────────────────────────────┘
```

---

## Navigation

### Enter a Folder
**Double-click** any folder row to navigate into it.

### Go Up
**Double-click** the `..` row at the top of a pane to go to the parent directory.

### Back and Forward
Use the **◀** and **▶** buttons in each pane's toolbar to move through your navigation history. Buttons are greyed out when there is no history in that direction. Each pane has its own independent history.

---

## Columns

| Column | Meaning |
|--------|---------|
| **Name** | File name (without extension) or folder name |
| **Ext** | File extension (cbr, cbz, csv…). Empty for folders |
| **Items** | Number of direct children inside a folder. Empty for files. `?` if unreadable |
| **Size** | File size in MiB, KiB, or B. Empty for folders |
| **Modified** | Last modified date and time |

---

## Sorting

Click any **column header** to sort by that column:
- First click → ascending ↑
- Click again → descending ↓
- The active sort column shows an arrow indicator

Sort rules by column:
- **Name**, **Ext** — alphabetic (case-insensitive)
- **Items**, **Size** — numeric (files/folders with no value sort to the bottom)
- **Modified** — chronological

The `..` row always stays pinned at the top regardless of sort order.

---

## Folder Preview (Space)

Quickly peek inside a folder without navigating into it:

1. **Hover** over a folder row, or **single-click** it to select it
2. Press **Space** — a preview overlay appears showing the folder's contents (name, ext, size)
3. Press **Esc** or click anywhere outside the overlay to close it

The overlay positions itself to the right of the row (or left if near the screen edge) and stays on screen even when hovering near the bottom.

This is especially useful for spotting folders with unexpectedly many files — sort by **Items ↓** to find them, then Space to inspect without losing your place.

---

## Filtering

Type in the **Filter** box at the bottom of a pane to narrow the list. Matches are case-insensitive and search the Name column. The filter clears automatically when you navigate to a different folder.

---

## Default Folders

| Pane | Default Path |
|------|-------------|
| Left | `/home/nesha/Downloads/comics_download/` |
| Right | `/mnt/extramedia/Comics/` |

To change the starting folder, navigate using double-click and the back/forward buttons.

---

## Troubleshooting

**Pane shows "Error: Path not allowed"**
- The path you navigated to is outside the allowed roots
- Restart and stay within the default folder trees

**Items column shows `?`**
- The subfolder exists but its contents cannot be read (permission denied)

**Port 8200 already in use**
```bash
lsof -i :8200
kill -9 <PID>
```

**Page shows old content after server restart**
- Hard refresh: `Ctrl+Shift+R`

---

## Version History

### v1.1 (2026-05-16)
- Space key opens folder preview overlay — hover or click a folder, press Space to peek inside
- Esc or click outside closes the overlay
- Overlay auto-positions to stay on screen near the hovered/clicked row

### v1.0 (2026-05-16)
- Initial release
- Dual-pane directory listing
- Double-click folder navigation with back/forward history per pane
- Sortable columns: Name, Ext, Items, Size, Modified
- Filter bar per pane (live name filter)
- Dark theme consistent with cp_downloads2comics

---

**Version**: v1.1
**Last Updated**: 2026-05-16
**Server**: `list_folder_items_server.py` (port 8200)
**UI**: `list_folder_items.html`
