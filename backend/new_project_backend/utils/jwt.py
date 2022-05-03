from datetime import datetime, timedelta

import jwt
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric.ed448 import Ed448PrivateKey

private_key = (
    Ed448PrivateKey.generate()
    .private_bytes(
        encoding=crypto_serialization.Encoding.PEM,
        format=crypto_serialization.PrivateFormat.PKCS8,
        encryption_algorithm=crypto_serialization.NoEncryption(),
    )
    .decode()
)


def create_token(user_id: int, expiration_seconds: int):
    payload = {
        'sub': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=expiration_seconds),
    }
    return jwt.encode(payload, private_key, 'EdDSA')


def get_user_id_from_token(token: str):
    try:
        payload = jwt.decode(token, private_key, ['EdDSA'], require=['sub', 'exp'])
        try:
            return int(payload['sub'])
        except ValueError:
            return None
    except jwt.InvalidTokenError:
        return None
