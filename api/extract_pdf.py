import os
import json
from http.server import BaseHTTPRequestHandler

import google.generativeai as genai

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)


class handler(BaseHTTPRequestHandler):

    def do_GET(self):

        try:

            models = []

            for m in genai.list_models():

                models.append({
                    "name": m.name,
                    "supported_generation_methods": getattr(
                        m,
                        "supported_generation_methods",
                        []
                    )
                })

            return self.send_json(
                200,
                {
                    "success": True,
                    "models": models
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

    def do_POST(self):

        return self.send_json(
            200,
            {
                "success": False,
                "message": "Modo de diagnóstico ativo"
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
                ensure_ascii=False,
                indent=2
            ).encode("utf-8")
        )
