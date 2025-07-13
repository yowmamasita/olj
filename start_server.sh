#!/bin/bash

echo "Starting HTTP server for Skills Mind Map..."
echo "Open http://localhost:8000/skills_mindmap.html in your browser"
echo "Press Ctrl+C to stop the server"

# Start Python HTTP server
python3 -m http.server 8000