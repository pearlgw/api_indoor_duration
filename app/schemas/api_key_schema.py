from pydantic import BaseModel
from datetime import datetime

class ApiKeyResponse(BaseModel):
    api_key: str
    expires_at: datetime

    class Config:
        from_attributes = True
