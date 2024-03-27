import time
from typing import Dict
import jwt
from config.config import Settings

def token_response(token: str):
    return {"access_token": token}

secret_key = Settings().secret_key
algorithm = Settings().algorithm

def sign_jwt(user_id: str) -> Dict[str, str]:
    payload = { "user_id": user_id, "expires": time.time() + 2400 }
    return token_response(jwt.encode(payload, secret_key, algorithm=algorithm))

def decode_jwt(token: str) -> dict:
    decoded_token = jwt.decode(token.encode(), secret_key, algorithms=[algorithm])
    return decoded_token if decoded_token["expires"] >= time.time() else {}
