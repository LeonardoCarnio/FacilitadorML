import json
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):

    def do_POST(self):

        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        data = json.loads(body)

        title = data.get("title", "")
        description = data.get("description", "")

        result = {
            "optimized_title": f"{title} | Produto Premium",
            "optimized_description": description,
            "keywords": [
                "mercado livre",
                "produto",
                "vendas"
            ]
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(
            json.dumps(result).encode()
        )
