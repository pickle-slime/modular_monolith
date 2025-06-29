from dataclasses import dataclass, field
import re
   
@dataclass(frozen=True)
class CommonEmailField:
    value: str = field(default="")
    _email_pattern: str = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    def __post_init__(self):
        if len(self.value) > 225:
            raise ValueError(f"{self.__class__.__name__}: max length of email is 225 symbols")
        elif bool(re.search(self._email_pattern, self.value)):
            raise ValueError(f"{self.__class__.__name__}: Incorrect email")
        
    def __str__(self):
        return self.value

