from pathlib import Path

from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric.ed448 import Ed448PrivateKey


class PrivateKey:
    def __init__(self, path: str):
        self._key = ''
        self._path = Path(path)

    def initialize(self):
        if self._path.exists():
            with self._path.open('r', encoding='utf-8') as file:
                self._key = file.read()
        else:
            with self._path.open('w', encoding='utf-8') as file:
                self._key = (
                    Ed448PrivateKey.generate()
                    .private_bytes(
                        encoding=crypto_serialization.Encoding.Raw,
                        format=crypto_serialization.PrivateFormat.Raw,
                        encryption_algorithm=crypto_serialization.NoEncryption(),
                    )
                    .decode()
                )
                file.write(self._key)

    def get(self):
        return self._key


private_key = PrivateKey('/key/id_ed448')
