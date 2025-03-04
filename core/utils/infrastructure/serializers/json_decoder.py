from core.utils.application.base_dto import DTO
import json

class PydanticJSONDecoder(json.JSONDecoder):
    @staticmethod
    def from_dict(dtos: list[type[DTO]]):
        def decode(d):
            if isinstance(d, dict):
                if "__class__" in d:
                    for dto in dtos:
                        if d["__class__"] == dto.__name__:
                            dto_data = {k: decode(v) for k, v in d.items() if k != "__class__"}
                            return dto(**dto_data)
                return {k: decode(v) for k, v in d.items()}
            elif isinstance(d, list):
                return [decode(item) for item in d]
            return d

        return decode