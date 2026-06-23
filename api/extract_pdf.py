from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):

    def do_POST(self):

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(
            json.dumps(
                {
                    "products": [
                        {
                            "name": "Produto Teste 1",
                            "price": 10.50
                        },
                        {
                            "name": "Produto Teste 2",
                            "price": 22.90
                        }
                    ]
                }
            ).encode()
        )
