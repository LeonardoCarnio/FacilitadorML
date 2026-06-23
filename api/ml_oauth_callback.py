import os
import json
import requests
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


class handler(BaseHTTPRequestHandler):

    def do_GET(self):

        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        code = params.get("code", [None])[0]

        if not code:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps({
                "status": "waiting",
                "message": "Aguardando authorization code do Mercado Livre"
            }).encode())

            return

        client_id = os.environ.get("ML_CLIENT_ID")
        client_secret = os.environ.get("ML_CLIENT_SECRET")
        redirect_uri = os.environ.get("ML_REDIRECT_URI")

        token_url = "https://api.mercadolibre.com/oauth/token"

        payload = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "redirect_uri": redirect_uri
        }

        try:

            response = requests.post(
                token_url,
                headers={
                    "accept": "application/json",
                    "content-type": "application/json"
                },
                json=payload,
                timeout=30
            )

            data = response.json()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(
                json.dumps(
                    {
                        "success": True,
                        "oauth_response": data
                    },
                    indent=2
                ).encode()
            )

        except Exception as e:

            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(
                json.dumps({
                    "success": False,
                    "error": str(e)
                }).encode()
            )
