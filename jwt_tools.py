# WIP: Not used
import secrets
import jwt


def get_jwt_tools():
    SECRET = secrets.token_bytes(32)
    ALGORITHM = "HS256"
    def encode(payload):
        return jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    def decode(token):
        return jwt.decode(token, SECRET, algorithm=ALGORITHM)
    return encode, decode

jwt_encode, jwt_decode = get_jwt_tools()