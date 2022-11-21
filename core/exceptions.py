class SecretExpiredError(Exception):
    def __init__(self) -> None:
        super().__init__("Secret Expired")


class SecretViewedError(Exception):
    def __init__(self) -> None:
        super().__init__("Secret Already Viewed")
