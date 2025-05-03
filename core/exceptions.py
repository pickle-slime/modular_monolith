#General Exceptions
class MissingRepositoryError(Exception):
    def __init__(self, message):
        super().__init__(message)

class InvalidForeignUUIDException(ValueError):
    def __init__(self, message):
        super().__init__(self, message)

#User Management Exceptions
class UserAlreadyExistsError(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)

#Review Management Exceptions
class MissingProductRatingError(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)
