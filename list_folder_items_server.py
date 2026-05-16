#!/usr/bin/env python3
"""Dual-pane folder listing server. Port 8200."""

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

PORT = 8200
SRC_DIR = "/home/nesha/Downloads/comics_download/"
DEST_DIR = "/mnt/extramedia/Comics"
ALLOWED_ROOTS = [Path(SRC_DIR).resolve(), Path(DEST_DIR).resolve()]
HTML_FILE = Path(__file__).parent / "list_folder_items.html"


def is_allowed(path: Path) -> bool:
    resolved = path.resolve()
    return any(
        resolved == root or str(resolved).startswith(str(root) + os.sep)
        for root in ALLOWED_ROOTS
    )


def format_size(n: int) -> str:
    if n >= 1024 ** 2:
        return f"{n / 1024 ** 2:.1f} MiB"
    if n >= 1024:
        return f"{n / 1024:.1f} KiB"
    return f"{n} B"


def format_date(ts: float) -> str:
    import datetime
    dt = datetime.datetime.fromtimestamp(ts)
    return dt.strftime("%d/%m/%y %I:%M %p")


def list_dir(path_str: str) -> dict:
    path = Path(path_str)
    if not path.is_dir():
        raise ValueError("Not a directory")
    if not is_allowed(path):
        raise PermissionError("Path not allowed")

    items = []
    with os.scandir(path) as it:
        for entry in sorted(it, key=lambda e: e.name.lower()):
            stat = entry.stat(follow_symlinks=False)
            if entry.is_dir(follow_symlinks=False):
                try:
                    items_count = len(list(os.scandir(entry.path)))
                except PermissionError:
                    items_count = None
                items.append({
                    "name": entry.name,
                    "ext": "",
                    "is_dir": True,
                    "items_count": items_count,
                    "size_bytes": None,
                    "size": None,
                    "mtime": stat.st_mtime,
                    "modified": format_date(stat.st_mtime),
                })
            else:
                name_parts = entry.name.rsplit(".", 1)
                stem = name_parts[0] if len(name_parts) == 2 else entry.name
                ext = name_parts[1] if len(name_parts) == 2 else ""
                size_bytes = stat.st_size
                items.append({
                    "name": stem,
                    "ext": ext,
                    "is_dir": False,
                    "items_count": None,
                    "size_bytes": size_bytes,
                    "size": format_size(size_bytes),
                    "mtime": stat.st_mtime,
                    "modified": format_date(stat.st_mtime),
                })

    parent = str(path.parent) if path.parent != path else None
    return {"path": str(path), "parent": parent, "items": items}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def send_json(self, code: int, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/":
            try:
                html = HTML_FILE.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", len(html))
                self.end_headers()
                self.wfile.write(html)
            except FileNotFoundError:
                self.send_json(404, {"error": "HTML file not found"})
        elif parsed.path == "/api/list":
            params = parse_qs(parsed.query)
            path_str = params.get("path", [None])[0]
            if not path_str:
                self.send_json(400, {"error": "path parameter required"})
                return
            try:
                result = list_dir(path_str)
                self.send_json(200, result)
            except PermissionError as e:
                self.send_json(403, {"error": str(e)})
            except (ValueError, OSError) as e:
                self.send_json(400, {"error": str(e)})
        else:
            self.send_json(404, {"error": "Not found"})


if __name__ == "__main__":
    server = HTTPServer(("", PORT), Handler)
    print(f"List Folder Items — http://localhost:{PORT}")
    print(f"  Left:  {SRC_DIR}")
    print(f"  Right: {DEST_DIR}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
