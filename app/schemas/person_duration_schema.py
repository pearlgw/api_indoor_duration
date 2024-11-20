from typing import List
from pydantic import BaseModel
from datetime import time, date
from app.schemas.detail_person_duration_schema import DetailPersonDurationBaseResponse

class PersonDurationBaseCreate(BaseModel):
    name: str

    class Config:
        from_attributes = True

class PersonDurationBaseResponse(BaseModel):
    id: int
    name: str
    total_duration: time
    created_at: date

    class Config:
        from_attributes = True

class MessageResponsePersonDurationBase(BaseModel):
    message: str

class PersonDurationWithDetailsResponse(BaseModel):
    id: int
    name: str
    total_duration: time
    created_at: date
    details: List[DetailPersonDurationBaseResponse]

    class Config:
        from_attributes = True
