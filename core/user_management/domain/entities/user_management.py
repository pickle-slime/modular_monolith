from ....utils.domain.entity import Entity
from ..interfaces.hosts.password_hasher import PasswordHasherHost

from dataclasses import dataclass, field
from datetime import datetime
import uuid

@dataclass(kw_only=True)
class User(Entity):
    username: str = field(default=None)
    email: str = field(default=None)
    hashed_password: str = field(default=None)
    first_name: str = field(default=None)
    last_name: str = field(default=None)
    date_joined: datetime = field(default=None)
    last_login: datetime = field(default=None)
    role: str = field(default="user")

    def check_password(self, password: str, password_hasher: PasswordHasherHost):
        return password_hasher.verify(password, self.hashed_password)
