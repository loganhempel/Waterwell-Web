"""Static server mimicking vercel.json cleanUrls + trailingSlash:false. Usage: python3 serve.py ROOT PORT"""
import http.server, os, sys, functools
ROOT, PORT = sys.argv[1], int(sys.argv[2])
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
    def translate_path(self, path):
        p = super().translate_path(path)
        if os.path.isfile(p): return p
        q = p.rstrip('/')
        if os.path.isfile(q + '.html'): return q + '.html'
        if os.path.isfile(os.path.join(q, 'index.html')): return os.path.join(q, 'index.html')
        return p
    def send_head(self):
        # no directory listing / redirect: serve index for dirs (trailingSlash false)
        return super().send_head()
http.server.ThreadingHTTPServer(('127.0.0.1', PORT), functools.partial(H, directory=ROOT)).serve_forever()
