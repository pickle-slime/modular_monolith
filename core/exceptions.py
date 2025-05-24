#User Management Exceptions
class UserAlreadyExistsError(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)

#Review Management Exceptions
class MissingProductRatingError(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)
