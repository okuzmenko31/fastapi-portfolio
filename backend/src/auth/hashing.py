from passlib.context import CryptContext

hash_content = CryptContext(schemes=['bcrypt'])


class Hashing:

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return hash_content.verify(password, hashed_password)

    @staticmethod
    def get_hashed_password(password: str) -> str:
        return hash_content.hash(password)
