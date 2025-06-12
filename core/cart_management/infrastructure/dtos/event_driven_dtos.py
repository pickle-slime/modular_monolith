from pydantic import BaseModel, Field
import uuid

class LoggedUserEventDTO(BaseModel):
    pub_uuid: uuid.UUID = Field(description="User's public uuid")

