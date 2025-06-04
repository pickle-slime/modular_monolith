from types import FrameType
import inspect

class ApplicationException(Exception):
    prefix: str = "[APPLICATION ERROR]"

    def __init__(self, msg: str):
        self.raw_msg = msg
        cls_name, method_name = self._handle_error_context()
        super().__init__(f"{self.prefix} {cls_name}.{method_name}: {msg} {self.prefix}")

    def _handle_error_context(self) -> tuple[str, str]:
        frame = self._find_user_frame()

        if not frame:
            return "UnknownClass", "UnknownMethod"
        
        if frame:
            self_obj = frame.f_locals.get("self")
            cls_name = self_obj.__class__.__name__ if self_obj is not None else "UnknownClass"
            method_name = frame.f_code.co_name
        else:
            return "UnknownClass", "UnknownMethod"

        return cls_name, method_name

    def _find_user_frame(self) -> FrameType | None:
        """
        Walks back the frame stack until it finds a frame
        that does NOT belong to an Exception class.
        """
        frame = inspect.currentframe()
        while frame:
            f_locals = frame.f_locals
            self_obj = f_locals.get("self")

            if not isinstance(self_obj, ApplicationException):
                return frame
            frame = frame.f_back

        return None

class ValidationError(ApplicationException):
    ...

class MissingProductRatingError(ValidationError):
    ...
