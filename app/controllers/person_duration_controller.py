import os
import re
from fastapi import HTTPException
from fastapi.responses import FileResponse
import pytz
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, time
from app.models import person_duration
from app.schemas.person_duration_schema import PersonDurationBaseCreate, PersonDurationBaseResponse, MessageResponsePersonDurationBase

def create_person_duration(db: Session, person_duration_base: PersonDurationBaseCreate):
    indonesia_timezone = pytz.timezone("Asia/Jakarta")
    
    today = datetime.now(indonesia_timezone).date()

    cleaned_name = re.sub(r'\d+', '', person_duration_base.name)

    total_duration = time(0, 0, 0)

    existing_entry = db.query(person_duration.PersonDuration).filter(
        person_duration.PersonDuration.name == cleaned_name,
        person_duration.PersonDuration.created_at == today
    ).first()

    if existing_entry:
        return MessageResponsePersonDurationBase(message="Data sudah ada untuk hari ini")

    new_entry = person_duration.PersonDuration(
        name=cleaned_name,
        total_duration=total_duration,
    )
    
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    
    return PersonDurationBaseResponse(
        id=new_entry.id,
        name=new_entry.name,
        total_duration=new_entry.total_duration,
        created_at=new_entry.created_at
    )

IMAGE_DIRECTORY = "uploaded_images"

def get_image(filename: str):
    try:
        file_path = os.path.join(IMAGE_DIRECTORY, filename)

        if not os.path.isfile(file_path):
            raise HTTPException(status_code=404, detail="File not found")

        abs_file_path = os.path.abspath(file_path)
        abs_image_dir = os.path.abspath(IMAGE_DIRECTORY)

        if not abs_file_path.startswith(abs_image_dir):
            raise HTTPException(status_code=403, detail="Access to the file is forbidden")

        return FileResponse(file_path, media_type="image/jpeg")

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving image: {str(e)}")
    
def get_all_person_durations_with_details(db: Session):
    person_durations = (
        db.query(person_duration.PersonDuration)
        .order_by(person_duration.PersonDuration.created_at.desc())
        .all()
    )
    return person_durations