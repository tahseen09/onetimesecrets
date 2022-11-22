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
    def create_secret(cls, data: str, days: int = 7) -> tuple:
        """Encrypts the data and save in the Database

        Args:
            data (str): plain text user data
            days (int, optional): Number of days to expire. Defaults to 7.

        Returns:
            tuple: Secret Database Object, The Password to Open the Secret
        """
        secret, nonce = Secret.encrypt(data, days)
        secret.save()
        return secret, nonce
