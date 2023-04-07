import json
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


class Model(BaseModel):  # type: ignore
    class Config:
        json_encoders = {UUID: str, datetime: lambda d: d.strftime(DATETIME_FORMAT)}

    def to_dict(self) -> Any:
        return json.loads(self.json())


class ToDo(Model):
    id: UUID

    created_at: datetime
    updated_at: datetime

    text: str
    done: bool


class ToDoCreation(Model):
    id: UUID = Field(default_factory=uuid4)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    text: str
    done: bool = False
