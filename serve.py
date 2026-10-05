#!/usr/bin/env python3
"""
Serves the Maples Tech Club website AND builds the application PDF on demand.

Every time someone clicks the download link, this checks what today's date is in
India. If the PDF on disk was not built today, it runs build_pdf.py again before
sending the file. So the application a visitor downloads is always dated the day
they downloaded it, never the day it happened to be built.

    python3 serve.py            # http://0.0.0.0:8080

Note: this needs a host that can run Python. GitHub Pages cannot - see the
.github/workflows/publish.yml workflow for the static-hosting answer.
"""
import http.server
import os
import socketserver
import subprocess
import sys
import threading
from datetime import datetime, timedelta, timezone

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(BASE, "maples-tech-club")
BUILDER = os.path.join(BASE, "build_pdf.py")
PDF_NAME = "Maples_Tech_Club_Proposal_Principal.pdf"
PDF_BUILT = os.path.join(BASE, PDF_NAME)
PORT = int(os.environ.get("PORT", 8080))

# India is permanently UTC+05:30, so a fixed offset is exact.
IST = timezone(timedelta(hours=5, minutes=30))

_lock = threading.Lock()
_cache = {"stamp": None, "data": None}


def _today():
    return datetime.now(IST).strftime("%Y-%m-%d")


def _builder_mtime():
    try:
        return os.path.getmtime(BUILDER)
    except OSError:
        return 0.0


def current_pdf():
    """Return the PDF bytes, rebuilding first if it wasn't built today."""
    stamp = (_today(), _builder_mtime())
    with _lock:
        if _cache["stamp"] == stamp and _cache["data"]:
            return _cache["data"], False

        rebuilt = False
        r = subprocess.run([sys.executable, BUILDER], capture_output=True, text=True)
        if r.returncode == 0:
            rebuilt = True
        else:
            sys.stderr.write("  ! build_pdf.py failed, serving the file already on disk\n")
            sys.stderr.write((r.stderr or "")[-400:] + "\n")

        with open(PDF_BUILT, "rb") as fh:
            data = fh.read()

        # keep the static copy inside the site folder in step as well
        try:
            with open(os.path.join(ROOT, PDF_NAME), "wb") as fh:
                fh.write(data)
        except OSError:
            pass

        _cache["stamp"], _cache["data"] = stamp, data
        if rebuilt:
            print(f"  [rebuilt] PDF dated {_today()}  -  {len(data):,} bytes", flush=True)
        return data, rebuilt


class Handler(http.server.SimpleHTTPRequestHandler):
    server_version = "MaplesTechClub"

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def _is_pdf(self):
        return self.path.split("?")[0].lstrip("/") == PDF_NAME

    def _send_pdf(self, body=True):
        data, _ = current_pdf()
        self.send_response(200)
        self.send_header("Content-Type", "application/pdf")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Content-Disposition",
                         f'attachment; filename="{PDF_NAME}"')
        # never let a browser or proxy hand back yesterday's dated copy
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.end_headers()
        if body:
            self.wfile.write(data)

    def do_GET(self):
        if self._is_pdf():
            return self._send_pdf(body=True)
        return super().do_GET()

    def do_HEAD(self):
        if self._is_pdf():
            return self._send_pdf(body=False)
        return super().do_HEAD()

    def end_headers(self):
        # the HTML is regenerated often; don't let the browser cache it either
        if not self._is_pdf():
            self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stdout.write("  %s %s\n" % (self.address_string(), fmt % args))
        sys.stdout.flush()


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    print(f"Maples Tech Club site  ->  http://0.0.0.0:{PORT}")
    print(f"  static files : {ROOT}")
    print(f"  /{PDF_NAME}")
    print("     rebuilt on download whenever the last build was not today (India time)")
    print()
    current_pdf()  # warm it up so the first click is instant
    with Server(("0.0.0.0", PORT), Handler) as httpd:
        httpd.serve_forever()
