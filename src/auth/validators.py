import re
from typing import NamedTuple, Optional


class PasswordValidationData(NamedTuple):
    error: Optional[str] = None
    success: Optional[bool] = None


class PasswordValidator:

    def __init__(self, value: str):
        self.password = value

    def check_lowercase(self):
        if not re.search("[a-z]", self.password):
            return PasswordValidationData(
                error='Password must contain letters a-z!'
            )

    def check_uppercase(self):
        if not re.search("[A-Z]", self.password):
            return PasswordValidationData(
                error='Password must contain letters A-Z!'
            )

    def check_numbers(self):
        if not re.search("[0-9]", self.password):
            return PasswordValidationData(
                error='Password must contain numbers 0-9!'
            )

    def check_length(self):
        if len(self.password) < 9:
            return PasswordValidationData(
                error='Password length must be more than 9 symbols!'
            )

    def check_all(self):
        check_lowercase = self.check_lowercase()
        check_uppercase = self.check_uppercase()
        check_numbers = self.check_numbers()
        check_length = self.check_length()

        if check_lowercase is not None:
            return check_lowercase
        elif check_uppercase is not None:
            return check_uppercase
        elif check_numbers is not None:
            return check_numbers
        elif check_length is not None:
            return check_length
        return None

    def validate_password(self):
        result = self.check_all()
        if result is None:
            return PasswordValidationData(success=True)
        return result


def validate_password(password: str) -> PasswordValidationData:
    validator = PasswordValidator(value=password)
    return validator.validate_password()


