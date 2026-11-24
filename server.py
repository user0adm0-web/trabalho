#!/usr/bin/env python3
"""
Servidor local para o seminário:
  Os povos das Américas e as conquistas

Execute:  python3 server.py
Acesse:   http://localhost:8080/apresentacao.html
"""

import http.server
import socketserver
import os
import sys
import webbrowser
import threading

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080

# Serve from the directory where this script lives
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Copy the connected presentation next to the server if it exists in parent
src = os.path.join(os.path.dirname(__file__), "..", "apresentacao.html")
dst = os.path.join(os.path.dirname(__file__), "apresentacao.html")
if os.path.exists(src) and not os.path.exists(dst):
    import shutil
    shutil.copy2(src, dst)

class Handler(http.server.SimpleHTTPRequestHandler):
    MIME = {
        ".html": "text/html; charset=utf-8",
        ".css":  "text/css; charset=utf-8",
        ".js":   "application/javascript; charset=utf-8",
        ".png":  "image/png",
        ".jpg":  "image/jpeg",
        ".svg":  "image/svg+xml",
        ".json": "application/json",
    }

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def guess_type(self, path):
        ext = os.path.splitext(path)[1].lower()
        return self.MIME.get(ext, super().guess_type(path))

    def log_message(self, fmt, *args):
        if "favicon" in str(args[0]):
            return
        print(f"  {self.address_string()}  {fmt % args}")


def main():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.allow_reuse_address = True
        url = f"http://localhost:{PORT}/apresentacao.html"

        print("=" * 54)
        print("  SEMINÁRIO — Os povos das Américas e as conquistas")
        print("=" * 54)
        print(f"  URL : {url}")
        print(f"  Dir : {os.getcwd()}")
        print("  Atalhos: ← → / Espaço | N = notas | F = tela cheia")
        print("  Pressione Ctrl+C para parar.\n")

        threading.Timer(0.8, lambda: webbrowser.open(url)).start()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n  Servidor encerrado.")


if __name__ == "__main__":
    main()
