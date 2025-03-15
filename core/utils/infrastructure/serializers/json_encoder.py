from pydantic import BaseModel
from datetime import datetime
import uuid
import json


class PydanticJSONEncoder(json.JSONEncoder):
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
        
        # if isinstance(obj, str) or isinstance(obj, int) or obj == None:
        #     return obj
        
        try:
            return super().default(obj)
        except TypeError:
            return str(obj)