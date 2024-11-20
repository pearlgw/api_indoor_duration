from datetime import datetime
import pytz
from sqlalchemy import Column, Integer, String, Time, Date
from sqlalchemy.orm import relationship
from app.config.config import Base

INDONESIA_TZ = pytz.timezone('Asia/Jakarta')

class PersonDuration(Base):
    __tablename__ = "person_durations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    total_duration = Column(Time, nullable=True)
    # Menetapkan default timezone ke Indonesia (WIB)
    created_at = Column(Date, default=lambda: datetime.now(INDONESIA_TZ).date(), nullable=False)

    details = relationship("DetailPersonDuration", back_populates="person_duration", lazy="joined")