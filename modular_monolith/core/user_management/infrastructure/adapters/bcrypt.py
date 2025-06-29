import bcrypt
from core.user_management.domain.interfaces.hosts.password_hasher import PasswordHasherHost

class BcryptPasswordHasherAdapter(PasswordHasherHost):
    def hash(self, password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt().decode())

    def verify(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())
