from datetime import datetime
import uuid
import os
from PIL import Image
import pytz
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import detail_person_duration, person_duration
from app.models.person_duration import PersonDuration
from app.schemas.detail_person_duration_schema import DetailPersonDurationBaseCreate

UPLOAD_FOLDER = "uploaded_images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def save_image(image_file) -> str:
    file_name = f"{uuid.uuid4()}.jpg"
    file_path = os.path.join(UPLOAD_FOLDER, file_name)

    with Image.open(image_file.file) as img:
        img = img.convert("RGB")
        img.save(file_path, "JPEG")

    return file_name

def create_detail_person_duration(
    nim: str,
    name: str,
    name_track_id: str,
    image_file,
    db: Session
):
    original_name = name
    
    cleaned_name = ''.join(filter(str.isalpha, name))
    cleaned_name_for_comparison = cleaned_name.replace(" ", "").lower()

    today = datetime.now(pytz.timezone('Asia/Jakarta')).date()

    matching_person_duration = db.query(person_duration.PersonDuration).filter(
        func.lower(func.replace(person_duration.PersonDuration.name, " ", "")) == cleaned_name_for_comparison,
        func.date(person_duration.PersonDuration.created_at) == today
    ).first()

    if not matching_person_duration:
        raise HTTPException(
            status_code=404, detail="Matching person_duration entry not found"
        )

    image_name = None
    if image_file:
        image_name = save_image(image_file)

    tz_indonesia = pytz.timezone('Asia/Jakarta')
    start_time_indonesia = datetime.now(tz_indonesia)

    start_time_formatted = start_time_indonesia.strftime('%Y-%m-%dT%H:%M:%S')

    new_detail = detail_person_duration.DetailPersonDuration(
        person_duration_id=matching_person_duration.id,
        labeled_image=image_name,
        nim=nim,
        name=original_name,
        name_track_id=name_track_id,
        start_time=start_time_formatted,
        end_time=None
    )

    db.add(new_detail)
    db.commit()
    db.refresh(new_detail)

    return new_detail

def update_end_time_by_track_name_id(track_name_id: str, end_time: datetime, db: Session):
    matching_person_duration = db.query(detail_person_duration.DetailPersonDuration).filter(
        detail_person_duration.DetailPersonDuration.name_track_id == track_name_id
    ).first()

    if not matching_person_duration:
        raise HTTPException(
            status_code=404, detail="Person duration entry not found"
        )

    if matching_person_duration.end_time:
        raise HTTPException(
            status_code=400, detail="End time already set, cannot update"
        )

    start_time_indonesia = matching_person_duration.start_time

    matching_person_duration.end_time = end_time

    if matching_person_duration.end_time and start_time_indonesia:
        duration = matching_person_duration.end_time - start_time_indonesia
        total_seconds = duration.total_seconds()

        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)

        total_duration = f"{hours:02}:{minutes:02}:{seconds:02}"

        person_duration_entry = db.query(person_duration.PersonDuration).filter(
            person_duration.PersonDuration.id == matching_person_duration.person_duration_id
        ).first()

        if person_duration_entry:
            if person_duration_entry.total_duration:
                old_hours = person_duration_entry.total_duration.hour
                old_minutes = person_duration_entry.total_duration.minute
                old_seconds = person_duration_entry.total_duration.second

                old_total_seconds = old_hours * 3600 + old_minutes * 60 + old_seconds

                new_total_seconds = old_total_seconds + int(total_seconds)

                new_hours = new_total_seconds // 3600
                new_minutes = (new_total_seconds % 3600) // 60
                new_seconds = new_total_seconds % 60

                new_total_duration = f"{new_hours:02}:{new_minutes:02}:{new_seconds:02}"

                person_duration_entry.total_duration = new_total_duration
            else:
                person_duration_entry.total_duration = total_duration

            db.commit()
            db.refresh(person_duration_entry)
        else:
            raise HTTPException(
                status_code=404, detail="PersonDuration entry not found"
            )

    db.commit()
    db.refresh(matching_person_duration)

    return matching_person_duration