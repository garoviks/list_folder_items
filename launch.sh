#!/bin/bash
cd "$(dirname "$0")"
pkill -f "list_folder_items_server" 2>/dev/null
sleep 1
python3 list_folder_items_server.py &
until nc -z localhost 8200 2>/dev/null; do sleep 0.2; done
xdg-open http://localhost:8200
