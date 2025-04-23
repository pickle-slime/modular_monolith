class MissingRepositoryError(Exception):
    def __init__(self, message):
        super().__init__(message)

class InvalidForeignUUIDException(ValueError):
    def __init__(self, message):
        super().__init__(self, message)

class UserAlreadyExistsError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
