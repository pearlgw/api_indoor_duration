import uuid
from sqlalchemy import Column, String, DateTime
from app.config.config import Base
from datetime import datetime, timedelta

class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    api_key = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=365))
