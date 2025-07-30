from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import date
from typing import Optional
from uuid import uuid4


class Campaign(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    description: Optional[str] = None
    start_date: date
    end_date: date
    segment_id: Optional[int] = None

    @field_validator("name")
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name must not be empty")
        return v

    @model_validator(mode="after")
    def validate_dates(self) -> "Campaign":
        if self.end_date < self.start_date:
            raise ValueError("end_date must be after start_date")
        return self
