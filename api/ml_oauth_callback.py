import os
import json
import requests
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

TOKEN_FILE = "/tmp/ml_token.json"

class handler(BaseHTTPRequestHandler):

```
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
                "message": "Aguardando autorização do Mercado Livre"
            }).encode()
        )

        return

    client_id = os.environ.get("ML_CLIENT_ID")
    client_secret = os.environ.get("ML_CLIENT_SECRET")
    redirect_uri = os.environ.get("ML_REDIRECT_URI")

    payload = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri
    }

    try:

        token_response = requests.post(
            "https://api.mercadolibre.com/oauth/token",
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
                json.dumps(oauth_data, indent=2).encode()
            )

            return

        with open(TOKEN_FILE, "w") as f:
            json.dump(oauth_data, f)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(
            json.dumps({
                "success": True,
                "message": "Mercado Livre conectado com sucesso",
                "user_id": oauth_data.get("user_id")
            }).encode()
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
```
