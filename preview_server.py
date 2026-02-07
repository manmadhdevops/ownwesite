import os
import runpy
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8000


def get_html():
    base = os.path.dirname(__file__)
    website_path = os.path.join(base, 'website')
    ns = runpy.run_path(website_path)
    handler = ns.get('lambda_handler')
    if not handler:
        return "<html><body><h1>Error: lambda_handler not found in 'website'</h1></body></html>"
    resp = handler({}, {})
    return resp.get('body', '')


class PreviewHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        html = get_html()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=UTF-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def log_message(self, format, *args):
        return


if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', PORT), PreviewHandler)
    print(f"Serving preview at http://127.0.0.1:{PORT} - press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        print('Server stopped')
