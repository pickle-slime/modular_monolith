from .exceptions import ApplicationException

class ACLError(ApplicationException):
    prefix: str = "[ACL ERROR]"

class ModelNotFoundACLError(ACLError):
    pass 

class ProductNotFoundACLError(ModelNotFoundACLError):
    pass

class SizeNotFoundACLError(ModelNotFoundACLError):
    pass
