import json
import re
import tempfile
import cgi
import fitz
from http.server import BaseHTTPRequestHandler


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
                full_text += "\n" + page.get_text()

            doc.close()

            products = []

            pattern = re.compile(
                r"(BOM-\d+)\s+(.+?)\s+CX:.*?1CX:\s*([\d,]+)",
                re.DOTALL
            )

            matches = pattern.findall(full_text)

            for sku, name, price in matches:

                name = " ".join(name.split())

                try:
                    price = float(
                        price.replace(".", "")
                             .replace(",", ".")
                    )
                except:
                    price = 0

                products.append({
                    "sku": sku.strip(),
                    "name": name.strip(),
                    "price": price,
                    "category": "",
                    "image_url": ""
                })

            return self.send_json(
                200,
                {
                    "success": True,
                    "products": products,
                    "total": len(products)
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
