import os
import json
import requests
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


class handler(BaseHTTPRequestHandler):

    def do_GET(self):

        try:

            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)

            code = params.get("code", [None])[0]

            if not code:
                return self.send_json(
                    400,
                    {
                        "success": False,
                        "message": "Código OAuth não recebido"
                    }
                )

            response = requests.post(
                "https://api.mercadolibre.com/oauth/token",
                data={
                    "grant_type": "authorization_code",
                    "client_id": os.getenv("ML_CLIENT_ID"),
                    "client_secret": os.getenv("ML_CLIENT_SECRET"),
                    "code": code,
                    "redirect_uri": os.getenv("ML_REDIRECT_URI")
                },
                timeout=30
            )

            result = response.json()

            if response.status_code != 200:
                return self.send_json(
                    response.status_code,
                    result
                )

            self.send_response(302)

            self.send_header(
                "Location",
                "https://facilitador-ml.vercel.app/?ml_connected=true"
            )

            self.end_headers()

        except Exception as e:

            return self.send_json(
                500,
                {
                    "success": False,
                    "error": str(e)
                }
            )

    def send_json(self, status, data):

        self.send_response(status)
        self.send_header(
            "Content-Type",
            "application/json"
        )
        self.end_headers()

        self.wfile.write(
            json.dumps(data).encode("utf-8")
        )
