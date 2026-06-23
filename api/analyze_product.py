import json
import requests
from http.server import BaseHTTPRequestHandler

TOKEN_FILE = "/tmp/ml_token.json"

class handler(BaseHTTPRequestHandler):

```
def do_GET(self):

    try:

        with open(TOKEN_FILE, "r") as f:
            token_data = json.load(f)

        access_token = token_data["access_token"]

        response = requests.get(
            "https://api.mercadolibre.com/users/me",
            headers={
                "Authorization": f"Bearer {access_token}"
            },
            timeout=30
        )

        user_data = response.json()

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(
            json.dumps({
                "connected": True,
                "user": user_data
            }).encode()
        )

    except FileNotFoundError:

        self.send_response(400)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(
            json.dumps({
                "connected": False,
                "message": "Nenhum token encontrado"
            }).encode()
        )

    except Exception as e:

        self.send_response(500)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(
            json.dumps({
                "error": str(e)
            }).encode()
        )
```
