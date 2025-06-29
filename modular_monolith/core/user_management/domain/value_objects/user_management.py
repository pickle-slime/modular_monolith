from dataclasses import dataclass
from typing import Literal, cast

@dataclass(frozen=True)
class RoleField:
    ValidRole = Literal['customer', 'guest', 'admin', 'manager']
    value: ValidRole | str = 'customer'

    def __post_init__(self):
        if self.value not in ('customer', 'guest', 'admin', 'manager'):
            raise ValueError(
                f"{self.__class__.__name__} accepts only one of: "
                f"'customer', 'guest', 'admin', 'manager'. Got: {self.value}"
            )

    def __str__(self) -> Literal['customer', 'guest', 'admin', 'manager']:
        return cast(RoleField.ValidRole, self.value)
