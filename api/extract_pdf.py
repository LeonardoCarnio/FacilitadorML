import os
import json
import tempfile
import cgi
import fitz
import google.generativeai as genai
from http.server import BaseHTTPRequestHandler

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-1.5-pro")


class handler(BaseHTTPRequestHandler):

    def do_POST(self):

        try:

            ctype, pdict = cgi.parse_header(
                self.headers.get("Content-Type")
            )

            if ctype != "multipart/form-data":
                return self.send_json(
                    400,
                    {
                        "success": False,
                        "error": "Esperado multipart/form-data"
                    }
                )

            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    "REQUEST_METHOD": "POST",
                    "CONTENT_TYPE": self.headers["Content-Type"]
                }
            )

            if "file" not in form:

                return self.send_json(
                    400,
                    {
                        "success": False,
                        "error": "Arquivo PDF não enviado"
                    }
                )

            pdf_file = form["file"]

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as temp:

                temp.write(pdf_file.file.read())
                pdf_path = temp.name

            doc = fitz.open(pdf_path)

            full_text = ""

            for page in doc:
                full_text += page.get_text()

            doc.close()

            prompt = f"""
Você receberá o texto de um catálogo PDF.

Extraia todos os produtos encontrados.

Retorne APENAS JSON válido.

Formato:

{{
  "products": [
    {{
      "name": "Nome do Produto",
      "price": 99.90,
      "category": "Categoria",
      "image_url": ""
    }}
  ]
}}

Texto:

{full_text[:150000]}
"""

            response = model.generate_content(prompt)

            text = response.text.strip()

            if text.startswith("```json"):
                text = text.replace("```json", "")
                text = text.replace("```", "")
                text = text.strip()

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

        return self.send_json(
            200,
            {
                "success": True,
                "endpoint": "extract_pdf",
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
