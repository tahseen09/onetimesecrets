from datetime import datetime, timedelta, timezone
from django.db import models

from core.services.crypto import Decryption, Encryption

from .base_model import BaseModel


class Secret(BaseModel):
    expire_at = models.DateTimeField()
    ciphertext = models.TextField(null=True, blank=True)
    tag = models.TextField(null=True, blank=True)
    is_viewed = models.BooleanField(default=False)

    def mark_viewed(self):
        self.is_viewed = True
        self.save()

    def decrypt(self, nonce: str) -> str:
        data = Decryption.decrypt(self.ciphertext, self.tag, nonce)
        self.mark_viewed()
        return data

    @classmethod
    def encrypt(cls, data: str, days: int = 7) -> tuple:
        """
        Args:
            data (str): Any string which needs to be encrypted

        Returns:
            tuple: Secret Object & Nonce value
        """
        ciphertext, tag, nonce = Encryption.encrypt(data)
        return (
            Secret(
                ciphertext=ciphertext,
                tag=tag,
                expire_at=datetime.now() + timedelta(days=days),
            ),
            nonce,
        )

    @property
    def is_active(self):
        return not self.is_expired and not self.is_viewed

    @property
    def is_expired(self):
        now = datetime.now()
        return now.astimezone(timezone.utc) >= self.expire_at.astimezone(timezone.utc)
