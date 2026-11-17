"""Local server for Sightline.

Like `python3 -m http.server`, plus:
  * no browser caching, so every reload picks up the latest files
  * /api/tmdb  -> forwards whitelisted TMDB requests with your key (same as the Vercel function)

Put your key in a file called .env.local next to this one:
    TMDB_API_KEY=your_key_here
(or export TMDB_API_KEY in your shell). Without a key the cinema uses its built-in films.

Run:  python3 serve.py        then open http://localhost:5173
"""
import http.server
import json
import os
import re
import socketserver
import urllib.error
import urllib.parse
import urllib.request

PORT = 5173
ROOT = os.path.dirname(os.path.abspath(__file__))
PATHS = [re.compile(r"^search/movie$"), re.compile(r"^movie/now_playing$"), re.compile(r"^movie/\d+$")]
PARAMS = ["query", "language", "region", "append_to_response", "include_image_language", "page"]


def tmdb_key():
    if os.environ.get("TMDB_API_KEY"):
        return os.environ["TMDB_API_KEY"].strip()
    env = os.path.join(ROOT, ".env.local")
    if os.path.exists(env):
        for line in open(env, encoding="utf-8"):
            if line.strip().startswith("TMDB_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Expires", "0")
        super().end_headers()

    def send_json(self, status, payload):
        body = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        if url.path.rstrip("/") != "/api/tmdb":
            return super().do_GET()
        q = urllib.parse.parse_qs(url.query)
        path = (q.get("path") or [""])[0]
        key = tmdb_key()
        if not key:
            return self.send_json(500, {"error": "TMDB_API_KEY is not configured (.env.local)"})
        if not any(p.match(path) for p in PATHS):
            return self.send_json(400, {"error": "path not allowed"})
        params = {"api_key": key, **{k: q[k][0] for k in PARAMS if k in q}}
        try:
            with urllib.request.urlopen(f"https://api.themoviedb.org/3/{path}?{urllib.parse.urlencode(params)}", timeout=10) as r:
                return self.send_json(r.status, r.read())
        except urllib.error.HTTPError as e:
            return self.send_json(e.code, e.read())
        except Exception:
            return self.send_json(502, {"error": "TMDB unreachable"})


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True


if __name__ == "__main__":
    with Server(("", PORT), Handler) as httpd:
        print(f"Sightline running at http://localhost:{PORT}  (Ctrl+C to stop)")
        httpd.serve_forever()
