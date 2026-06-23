import os
import json
from http.server import BaseHTTPRequestHandler
import google.generativeai as genai

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)


class handler(BaseHTTPRequestHandler):

    def do_POST(self):

        try:

            content_length = int(
                self.headers.get("Content-Length", 0)
            )

            body = self.rfile.read(content_length)

            data = json.loads(body)

            name = data.get("name", "")

            model_name = "models/gemini-2.0-flash"

            model = genai.GenerativeModel(
                model_name
            )

            prompt = f"""
Analise este produto do catálogo.

Produto:
{name}

Retorne APENAS JSON válido:

{{
  "categoryId":"MLB1000",
  "categoryName":"Categoria",
  "categoryFee":11,
  "weightG":500,
  "dimensions": {{
    "c":20,
    "l":15,
    "a":10
  }},
  "suggestedShippingMode":"full"
}}
"""

            response = model.generate_content(
                prompt
            )

            text = response.text.strip()

            if text.startswith("```json"):
                text = text.replace(
                    "```json",
                    ""
                ).replace(
                    "```",
                    ""
                ).strip()

            result = json.loads(text)

            return self.send_json(
                200,
                result
            )

        except Exception as e:

            return self.send_json(
                500,
                {
                    "success": False,
                    "error": str(e)
                }
            )

    def do_GET(self):

        self.send_json(
            200,
            {
                "success": True,
                "endpoint": "analyze_product",
                "status": "online"
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
