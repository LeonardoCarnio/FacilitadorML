```python
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
                self.send_json(
                    200,
                    {
                        "success": False,
                        "message": "Nenhum código OAuth recebido"
                    }
                )
                return

            client_id = os.getenv("ML_CLIENT_ID")
            client_secret = os.getenv("ML_CLIENT_SECRET")
            redirect_uri = os.getenv("ML_REDIRECT_URI")

            if not client_id or not client_secret or not redirect_uri:
                self.send_json(
                    500,
                    {
                        "success": False,
                        "error": "Variáveis de ambiente não configuradas"
                    }
                )
                return

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

            oauth_data = response.json()

            if response.status_code != 200:
                self.send_json(
                    response.status_code,
                    {
                        "success": False,
                        "mercadolivre_response": oauth_data
                    }
                )
                return

            self.send_json(
                200,
                {
                    "success": True,
                    "message": "Mercado Livre conectado com sucesso",
                    "user_id": oauth_data.get("user_id"),
                    "access_token": oauth_data.get("access_token"),
                    "refresh_token": oauth_data.get("refresh_token")
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

    def send_json(self, status, data):

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(
            json.dumps(data).encode("utf-8")
        )
```
