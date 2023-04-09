import json
from datetime import datetime
from typing import Any, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Extra, Field

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


class Model(BaseModel):  # type: ignore
    class Config:
        json_encoders = {UUID: str, datetime: lambda d: d.strftime(DATETIME_FORMAT)}
        extra = Extra.forbid

    def to_dict(self) -> Any:
        return json.loads(self.json())


class ToDo(Model):
    id: UUID

    created_at: datetime
    updated_at: datetime

    task: str
    done: bool


class ToDoCreation(Model):
    id: UUID = Field(default_factory=uuid4)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    task: str
    done: bool = False


class ToDoUpdate(Model):
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    task: Optional[str] = None
    done: Optional[bool] = None
