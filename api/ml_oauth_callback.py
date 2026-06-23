import os
import json
import requests
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


class handler(BaseHTTPRequestHandler):

    def do_GET(self):

        try:

            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)

            code = query_params.get("code", [None])[0]

            if not code:
                return self.send_json(
                    400,
                    {
                        "success": False,
                        "message": "Código OAuth não recebido"
                    }
                )

            client_id = os.getenv("ML_CLIENT_ID")
            client_secret = os.getenv("ML_CLIENT_SECRET")
            redirect_uri = os.getenv("ML_REDIRECT_URI")

            if not client_id:
                return self.send_json(
                    500,
                    {"success": False, "error": "ML_CLIENT_ID não configurado"}
                )

            if not client_secret:
                return self.send_json(
                    500,
                    {"success": False, "error": "ML_CLIENT_SECRET não configurado"}
                )

            if not redirect_uri:
                return self.send_json(
                    500,
                    {"success": False, "error": "ML_REDIRECT_URI não configurado"}
                )

            response = requests.post(
                "https://api.mercadolibre.com/oauth/token",
                data={
                    "grant_type": "authorization_code",
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "code": code,
                    "redirect_uri": redirect_uri
                },
                timeout=30
            )

            result = response.json()

            if response.status_code != 200:

                return self.send_json(
                    response.status_code,
                    {
                        "success": False,
                        "mercadolivre_response": result
                    }
                )

            return self.send_json(
                200,
                {
                    "success": True,
                    "message": "Mercado Livre conectado com sucesso",
                    "user_id": result.get("user_id"),
                    "access_token": result.get("access_token"),
                    "refresh_token": result.get("refresh_token")
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
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()

        self.wfile.write(
            json.dumps(
                data,
                ensure_ascii=False
            ).encode("utf-8")
        )
