from .exceptions import ApplicationException

class ACLException(ApplicationException):
    prefix: str = "[ACL ERROR]"

class NotFoundWishlistACLError(ACLException):
    pass

class NotFoundCartACLError(ACLException):
    pass
