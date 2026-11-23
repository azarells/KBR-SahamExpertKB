# -*- coding: utf-8 -*-
"""Server dashboard SahamExpertKB (tanpa instalasi tambahan, hanya Python standar).

Tugasnya dua:
  1. Menyajikan halaman dashboard (dashboard/index.html) di http://localhost:8080
  2. Meneruskan (proxy) setiap permintaan /fuseki/... ke server Fuseki (default http://localhost:3030/...)
     sehingga browser hanya berbicara ke satu alamat — tidak ada masalah CORS.

Pakai (Fuseki harus sudah menyala lebih dulu, lihat output/fuseki/start_fuseki.sh):
    python3 dashboard/server.py
    python3 dashboard/server.py --port 8080 --fuseki http://localhost:3030 --no-browser
"""
import argparse, http.server, os, socketserver, sys, urllib.error, urllib.request, webbrowser

HERE = os.path.dirname(os.path.abspath(__file__))


def buat_handler(fuseki):
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=HERE, **kw)

        def log_message(self, fmt, *args):  # log ringkas
            if "/fuseki/" in self.path:
                sys.stderr.write("  [SPARQL] %s %s -> %s\n" % (self.command, self.path.split("?")[0], args[1] if len(args) > 1 else ""))

        def _proxy(self):
            target = fuseki.rstrip("/") + self.path[len("/fuseki"):]
            body = None
            if self.command == "POST":
                body = self.rfile.read(int(self.headers.get("Content-Length", 0) or 0))
            req = urllib.request.Request(target, data=body, method=self.command)
            for h in ("Content-Type", "Accept"):
                if self.headers.get(h):
                    req.add_header(h, self.headers[h])
            try:
                with urllib.request.urlopen(req, timeout=120) as r:
                    data, status, ctype = r.read(), r.status, r.headers.get("Content-Type", "text/plain")
            except urllib.error.HTTPError as e:
                data, status, ctype = e.read(), e.code, e.headers.get("Content-Type", "text/plain")
            except Exception as e:  # Fuseki mati / alamat salah
                data, status, ctype = ("Fuseki tidak bisa dihubungi di %s (%s). Sudah menjalankan start_fuseki.sh?" % (fuseki, e)).encode(), 502, "text/plain; charset=utf-8"
            self.send_response(status)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            if self.path.startswith("/fuseki/"):
                return self._proxy()
            return super().do_GET()

        def do_POST(self):
            if self.path.startswith("/fuseki/"):
                return self._proxy()
            self.send_error(405)
    return Handler


def main():
    ap = argparse.ArgumentParser(description="Server dashboard SahamExpertKB")
    ap.add_argument("--port", type=int, default=8080)
    ap.add_argument("--fuseki", default="http://localhost:3030", help="alamat server Fuseki")
    ap.add_argument("--no-browser", action="store_true", help="jangan buka browser otomatis")
    a = ap.parse_args()
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("127.0.0.1", a.port), buat_handler(a.fuseki)) as srv:
        url = "http://localhost:%d" % a.port
        print("Dashboard SahamExpertKB berjalan di  %s" % url)
        print("Permintaan SPARQL diteruskan ke       %s  (dataset /saham dan /saham-pellet)" % a.fuseki)
        print("Tekan Ctrl+C untuk berhenti.\n")
        if not a.no_browser:
            webbrowser.open(url)
        try:
            srv.serve_forever()
        except KeyboardInterrupt:
            print("\nDashboard dihentikan.")


if __name__ == "__main__":
    main()
