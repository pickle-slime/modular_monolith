from ..application.acl.user_management import UserACL
from ..infrastructure.repositories.user_management import DjangoUserRepository

class UserManagementACLFactory:
    '''
    The factory is dedicated to hiding initiation details of ACLs from other bounded contexts
    '''
    @staticmethod
    def create_user_acl() -> UserACL:
        return UserACL(DjangoUserRepository())