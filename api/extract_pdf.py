import os
import json
import tempfile
from http.server import BaseHTTPRequestHandler

import google.generativeai as genai
import fitz  # PyMuPDF

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)


class handler(BaseHTTPRequestHandler):

    def do_POST(self):

        try:

            self.send_json(
                501,
                {
                    "success": False,
                    "message": "Upload de PDF ainda não implementado neste endpoint. Use extract_text.py ou envie o conteúdo dele para correção."
                }
            )

        except Exception as e:

            self.send_json(
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
