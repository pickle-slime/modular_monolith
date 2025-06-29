from django.contrib.auth.hashers import make_password, check_password

from core.user_management.domain.interfaces.hosts.password_hasher import PasswordHasherHost

class DjangoPasswordHasherAdapter(PasswordHasherHost):
    """
    Adapter to encapsulate Django's password hashing and verification logic.
    """
    def hash(self, password: str) -> str:
        return str(make_password(password))

    def verify(self, password: str, hashed_password: str) -> bool:
        return check_password(password, hashed_password)
