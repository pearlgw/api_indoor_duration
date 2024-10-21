from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime # type: ignore
from sqlalchemy.sql import func # type: ignore
from database import Base
import pytz # type: ignore
from datetime import datetime, timedelta

class APIKeys(Base):
    __tablename__ = 'api_keys'

    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)

    def __init__(self, api_key: str):
        self.api_key = api_key
        jakarta_tz = pytz.timezone('Asia/Jakarta')
        self.created_at = datetime.now(jakarta_tz)
        self.expires_at = self.created_at + timedelta(days=365)  # 1 tahun

class PersonDurations(Base):
    __tablename__ = 'person_durations'

    id = Column(Integer, primary_key=True, index=True)
    labeled_image = Column(String)
    nim = Column(String)
    name = Column(String)
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True), nullable=True)

    def __init__(self, labeled_image: str, nim: str, name: str):
        self.labeled_image = labeled_image
        self.nim = nim
        self.name = name
        jakarta_tz = pytz.timezone('Asia/Jakarta')
        self.start_time = datetime.now(jakarta_tz)