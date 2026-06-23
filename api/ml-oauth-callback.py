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

            self.wfile.write(
                json.dumps({
                    "status": "waiting",
                    "message": "Aguardando authorization code do Mercado Livre"
                }).encode()
            )
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

            token_response = requests.post(
                token_url,
                headers={
                    "accept": "application/json",
                    "content-type": "application/json"
                },
                json=payload,
                timeout=30
            )

            oauth_data = token_response.json()

            if "access_token" not in oauth_data:

                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()

                self.wfile.write(
                    json.dumps(
                        {
                            "success": False,
                            "oauth_response": oauth_data
                        },
                        indent=2
                    ).encode()
                )
                return

            access_token = oauth_data["access_token"]

            user_response = requests.get(
                "https://api.mercadolibre.com/users/me",
                headers={
                    "Authorization": f"Bearer {access_token}"
                },
                timeout=30
            )

            user_data = user_response.json()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(
                json.dumps(
                    {
                        "success": True,
                        "oauth_response": oauth_data,
                        "user_data": user_data
                    },
                    indent=2
                ).encode()
            )

        except Exception as e:

            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(
                json.dumps(
                    {
                        "success": False,
                        "error": str(e)
                    },
                    indent=2
                ).encode()
            )
