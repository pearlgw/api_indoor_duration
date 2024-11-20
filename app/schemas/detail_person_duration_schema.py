from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DetailPersonDurationBaseCreate(BaseModel):
    labeled_image: Optional[str] = None
    nim: str
    name: str
    name_track_id: str

    class Config:
        from_attributes = True

class DetailPersonDurationBaseResponse(BaseModel):
    person_duration_id: int
    labeled_image: Optional[str] = None
    nim: str
    name: str
    name_track_id: str
    start_time: datetime
    end_time: Optional[datetime] = None

    class Config:
        from_attributes = True

class PersonDurationResponseUpdate(BaseModel):
    name_track_id: str
    end_time: datetime

class EndTimeUpdateRequest(BaseModel):
    end_time: datetime