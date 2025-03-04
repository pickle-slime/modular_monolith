from dataclasses import dataclass, field

@dataclass(frozen=True)
class ImageField:
    value: str = field(default=None)

    def __str__(self):
        return self.value

@dataclass(frozen=True)
class PercentageField:
    value: int = field(default=None)

    def __int__(self):
        return int(self.value)

