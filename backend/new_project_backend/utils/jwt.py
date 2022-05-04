from datetime import datetime, timedelta

import jwt

from .key import private_key


def create_token(user_id: int, expiration_seconds: int):
    payload = {
        'sub': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=expiration_seconds),
    }
    return jwt.encode(payload, private_key.get(), 'EdDSA')


def get_user_id_from_token(token: str):
    try:
        payload = jwt.decode(token, private_key.get(), ['EdDSA'], require=['sub', 'exp'])
        try:
            return int(payload['sub'])
        except ValueError:
            return None
    except jwt.InvalidTokenError:
        return None
