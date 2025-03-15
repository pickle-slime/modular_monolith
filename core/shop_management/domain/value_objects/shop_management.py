from dataclasses import dataclass, field

@dataclass(frozen=True)
class ImageField:
    value: str = field(default="")

    def __str__(self):
        return self.value

@dataclass(frozen=True)
class PercentageField:
    value: int = field(default=0)

    def __int__(self):
        return int(self.value)

