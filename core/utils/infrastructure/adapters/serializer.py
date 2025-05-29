from core.utils.domain.interfaces.hosts.serializer import SerializeHost
from core.utils.application.base_dto import DTO

from typing import Any, Callable
from pydantic import BaseModel
from datetime import datetime
import uuid
import json

class SerializeAdapter(SerializeHost):
    class _Decoder(json.JSONDecoder):
        @staticmethod
        def from_dict(dtos: list[type[DTO]]) -> Callable[[Any], Any]:
            def decode(d: Any) -> Any:
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

    class _Encoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, BaseModel):
                # Recursively encode DTOs while preserving structure
                return {key: self.default(value) for key, value in obj.model_dump().items()} | {"__class__": obj.__class__.__name__}
            if isinstance(obj, list):
                return [self.default(item) for item in obj] 
            if isinstance(obj, dict):
                return {key: self.default(value) for key, value in obj.items()}
            if isinstance(obj, uuid.UUID):
                return str(obj)
            if isinstance(obj, datetime):
                return obj.isoformat()
           
            try:
                return super().default(obj)
            except TypeError:
                return str(obj)

    def serialize(self, raw_data) -> str:
        return json.dumps(raw_data, cls=self._Encoder)

    def deserialize(self, serialized_data: str, dtos: list[type[DTO]] | None = None) -> Any:
        if dtos:
            return json.loads(serialized_data, object_hook=self._Decoder.from_dict(dtos))
        else:
            return json.loads(serialized_data)
