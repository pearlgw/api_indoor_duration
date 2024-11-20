from sqlalchemy import Column, Integer, String, func, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.config.config import Base

class DetailPersonDuration(Base):
    __tablename__ = "detail_person_durations"

    id = Column(Integer, primary_key=True, index=True)
    person_duration_id = Column(Integer, ForeignKey("person_durations.id"), nullable=False)
    labeled_image = Column(String, nullable=True)
    nim = Column(String, nullable=False)
    name = Column(String, nullable=False)
    name_track_id = Column(String, nullable=False)
    start_time = Column(DateTime, default=func.now(), nullable=False)
    end_time = Column(DateTime, nullable=True)

    person_duration = relationship("PersonDuration", back_populates="details")