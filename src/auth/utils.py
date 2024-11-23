import jwt

from src import config


class Token():
    def __init__(self, encoded_token, decoded_token):
        self.encoded = encoded_token
        self.decoded = decoded_token

    @classmethod
    def from_encoded(cls, encoded_token) -> 'Token':
        decoded = jwt.decode(
                    encoded_token,
                    options={"verify_signature": False}
                )

        return cls(encoded_token, decoded)

    @classmethod
    def generate(cls, email) -> 'Token':
        header = {
            'typ': 'jwt',
            'alg': config.JWT_ALGORITHM
        }
        payload = {
            'email': email
        }

        encoded_token = jwt.encode(
            headers=header,
            payload=payload,
            key=config.JWT_KEY,
            algorithm=config.JWT_ALGORITHM
        )
        decoded_token = payload

        return cls(encoded_token, decoded_token)

    def is_valid(self) -> bool:
        try:
            jwt.decode(self.encoded, config.JWT_KEY, algorithms=[config.JWT_ALGORITHM])
            return True

        except jwt.InvalidTokenError:
            return False

    @property
    def email(self) -> str:
        return self.decoded['email']
