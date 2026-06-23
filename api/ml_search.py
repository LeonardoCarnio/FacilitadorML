import json
import requests
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):

    def do_POST(self):

        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        data = json.loads(body)

        query = data.get("query", "")

        url = f"https://api.mercadolibre.com/sites/MLB/search?q={query}"

        response = requests.get(url)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(response.text.encode())
