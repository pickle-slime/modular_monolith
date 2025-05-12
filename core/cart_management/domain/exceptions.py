import inspect

class DomainException(Exception):
    prefix: str = "[DOMAIN ERROR]"

    def __init__(self, msg: str):
        cls_name, method_name = self._handle_error_context()
        super().__init__(f"{self.prefix} {cls_name}.{method_name}: {msg} {self.prefix}")

    def _handle_error_context(self) -> tuple[str, str]:
        frame = inspect.currentframe()

        if frame:
            frame = frame.f_back
        else:
            return "UnknownClass", "UnknownMethod"
        
        if frame:
            cls_name = frame.f_globals.get("self").__class__.__name__ if hasattr(frame.f_globals.get("self", None), "__class__") else "UnknownClass"
            method_name = frame.f_code.co_name
        else:
            return "UnknownClass", "UnknownMethod"

        return cls_name, method_name


class ValidationError(DomainException):
    prefix: str = "[DOMAIN VALIDATION ERROR]"

class InvalidSizeError(ValidationError):
    pass

class InvalidPriceError(ValidationError):
    pass
