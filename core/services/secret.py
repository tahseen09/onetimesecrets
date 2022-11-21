from typing import Union
from uuid import UUID
from core.exceptions import SecretExpiredError, SecretViewedError

from core.models.ots import Secret


class SecretService:
    @classmethod
    def get_secret_data(cls, secret_id: Union[str, UUID], nonce: str) -> str:
        secret = Secret.objects.get(id=secret_id)
        if secret.is_expired:
            raise SecretExpiredError

        if secret.is_viewed:
            raise SecretViewedError

        return secret.decrypt(nonce)

    @classmethod
    def create_secret(cls, data: str, days: int = 7) -> str:
        secret, nonce = Secret.encrypt(data, days)
        secret.save()
        return nonce
