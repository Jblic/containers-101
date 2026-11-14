"""Cat web app for the Containers 101 exercise.

This app shows one picture: the file luci-sitting.png in the same folder.
It uses only the Python standard library.
You do not need to change this file or to know Python.
"""
import html
import mimetypes
import signal
import socket
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

PORT = 8000
CAT_NAME = "Luci"
PICTURE_NAME = "luci-sitting.png"
PICTURE = Path(__file__).parent / PICTURE_NAME
PICTURE_TYPE = mimetypes.guess_type(PICTURE_NAME)[0] or "application/octet-stream"

PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{name}</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 3rem auto; max-width: 44rem; padding: 0 1rem; text-align: center; color: #0f1b2d; }}
    img {{ max-width: 100%; border-radius: 12px; }}
    .note {{ color: #5c6878; }}
    .problem {{ padding: 3rem 1rem; border: 2px dashed #a83c08; border-radius: 12px; color: #a83c08; }}
  </style>
</head>
<body>
  <h1>This is {name}</h1>
  {picture}
  <p class="note">Container {hostname} sent you this page.</p>
</body>
</html>
"""

PICTURE_OK = '<img src="/{file}" alt="A picture of {name}">'
PICTURE_MISSING = '<p class="problem">The file {file} is not in this container. Copy it into the image.</p>'


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_page()
        elif self.path == "/" + PICTURE_NAME and PICTURE.is_file():
            self.send_bytes(PICTURE.read_bytes(), PICTURE_TYPE)
        else:
            self.send_error(404)

    def send_page(self):
        name = html.escape(CAT_NAME)
        template = PICTURE_OK if PICTURE.is_file() else PICTURE_MISSING
        picture = template.format(file=html.escape(PICTURE_NAME), name=name)
        page = PAGE.format(name=name, picture=picture, hostname=html.escape(socket.gethostname()))
        self.send_bytes(page.encode("utf-8"), "text/html; charset=utf-8")

    def send_bytes(self, body, content_type):
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def stop(signum, frame):
    print("Stop signal received. The app stops.", flush=True)
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    print(f"The cat app listens on port {PORT}.", flush=True)
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
