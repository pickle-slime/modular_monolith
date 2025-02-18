class MissingRepositoryError(Exception):
    def __init__(self, message):
        super().__init__(message)

class InvalidFilterTypeException(ValueError):
    def __init__(self, message):
        super().__init__(self, message)

class InvalidForeignUUIDException(ValueError):
    def __init__(self, message):
        super().__init__(self, message)