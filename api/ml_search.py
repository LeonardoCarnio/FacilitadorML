import json
import requests
from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):

    def do_POST(self):

        try:

            content_length = int(
                self.headers.get("Content-Length", 0)
            )

            body = self.rfile.read(content_length)

            data = json.loads(body)

            query = data.get("query", "").strip()

            if not query:

                return self.send_json(
                    400,
                    {
                        "success": False,
                        "error": "query vazia"
                    }
                )

            url = (
                "https://api.mercadolibre.com/"
                f"sites/MLB/search?q={query}&limit=10"
            )

            response = requests.get(
                url,
                timeout=20
            )

            result = response.json()

            products = []

            for item in result.get("results", []):

                products.append({
                    "id": item.get("id"),
                    "title": item.get("title"),
                    "price": item.get("price"),
                    "permalink": item.get("permalink"),
                    "thumbnail": item.get("thumbnail")
                })

            return self.send_json(
                200,
                {
                    "success": True,
                    "query": query,
                    "products": products
                }
            )

        except Exception as e:

            return self.send_json(
                500,
                {
                    "success": False,
                    "error": str(e)
                }
            )

    def send_json(self, status_code, data):

        self.send_response(status_code)
        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )
        self.end_headers()

        self.wfile.write(
            json.dumps(
                data,
                ensure_ascii=False
            ).encode("utf-8")
        )
