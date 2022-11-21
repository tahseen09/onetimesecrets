from Crypto.Cipher import AES

from core.constants import ENCRYPTION_KEY


MODE = AES.MODE_EAX
ENCODING_FORMAT = "utf-8"


class Encryption:
    @classmethod
    def encrypt(cls, data: str) -> tuple:
        data = data.encode(ENCODING_FORMAT)
        cipher = AES.new(ENCRYPTION_KEY, MODE)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        nonce = cipher.nonce
        return ciphertext.hex(), tag.hex(), nonce.hex()


class Decryption:
    @classmethod
    def decrypt(cls, ciphertext: str, tag: str, nonce: str):
        ciphertext = bytes.fromhex(ciphertext)
        tag = bytes.fromhex(tag)
        nonce = bytes.fromhex(nonce)
        cipher = AES.new(ENCRYPTION_KEY, MODE, nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)
        data = data.decode(ENCODING_FORMAT)
        return data

