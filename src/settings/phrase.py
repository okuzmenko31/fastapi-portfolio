import json


class SecretPhrase:
    file_path: str = None

    @staticmethod
    def secret_file_default_path():
        return 'secret_phrase/secret_phrase.json'

    def get_phrase_json(self):
        path = self.file_path
        if self.file_path is None:
            path = self.secret_file_default_path()
        with open(path) as secret_phrase:
            phrases_dict = secret_phrase.read()
        return phrases_dict

    def get_secret_phrase(self) -> str:
        phrase_dict = json.loads(self.get_phrase_json())
        phrase = phrase_dict['phrase']
        return phrase

    def check_secret_phrase(self, phrase: str) -> bool:
        return phrase == self.get_secret_phrase()


def check_phrase_is_valid(phrase: str):
    secret = SecretPhrase()
    return secret.check_secret_phrase(phrase)
