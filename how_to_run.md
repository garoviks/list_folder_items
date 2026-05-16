# List Folder Items — How to Run

## Prerequisites

- Python 3.8+
- Directories accessible:
  - `/home/nesha/Downloads/comics_download/`
  - `/mnt/extramedia/Comics/`

---

## Start the Server

```bash
cd /home/nesha/scripts/list_folder_items
python3 list_folder_items_server.py
```

Output:
```
List Folder Items — http://localhost:8200
  Left:  /home/nesha/Downloads/comics_download/
  Right: /mnt/extramedia/Comics
```

Keep this terminal open. Press **Ctrl+C** to stop.

---

## Open in Browser

```
http://localhost:8200
```

Both panes load immediately with the default folders.

---

## File Structure

```
/home/nesha/scripts/list_folder_items/
├── list_folder_items_server.py     (HTTP server, port 8200)
├── list_folder_items.html          (web UI)
├── how_to_run.md                   (this file)
├── LIST_FOLDER_ITEMS_ARCHITECTURE.md
├── LIST_FOLDER_ITEMS_REQUIREMENTS.md
└── LIST_FOLDER_ITEMS_USER_GUIDE.md
```

---

## No Dependencies

Standard library only. No `pip install` needed.
