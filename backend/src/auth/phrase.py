import os

from dotenv import load_dotenv

load_dotenv()


class SecretPhrase:
    secret_phrase = os.getenv('SECRET_PHRASE', 'secret_phrase')

    def check_secret_phrase(self, phrase: str) -> bool:
        return phrase == self.secret_phrase


def check_phrase_is_valid(phrase: str):
    secret = SecretPhrase()
    return secret.check_secret_phrase(phrase)
