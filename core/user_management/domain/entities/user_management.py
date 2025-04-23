from core.utils.domain.entity import Entity
from core.user_management.domain.value_objects.user_management import RoleField
from ..interfaces.hosts.password_hasher import PasswordHasherHost

from dataclasses import dataclass, field
from datetime import datetime

@dataclass(kw_only=True)
class User(Entity):
    username: str | None = field(default=None)
    email: str | None = field(default=None)
    hashed_password: str | None = field(default=None)
    first_name: str | None = field(default=None)
    last_name: str | None = field(default=None)
    date_joined: datetime | None = field(default=None)
    last_login: datetime | None = field(default=None)
    role: RoleField | str | None = field(default=None)

    def __post_init__(self):
        if isinstance(self.role, str):
            object.__setattr__(self, 'role', RoleField(self.role))

    def check_password(self, password: str, password_hasher: PasswordHasherHost):
        if self.hashed_password:
            return password_hasher.verify(password, self.hashed_password)
        else:
            raise ValueError(f"{self.__class__.__name__}.{self.__class__.check_password.__name__}: tried to check password while the hashed_password is None")

    @staticmethod
    def guest() -> 'User':
        return User(role=RoleField('guest'))
