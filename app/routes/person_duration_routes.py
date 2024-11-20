from typing import List
from datetime import datetime
import os
from typing import Union
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.config.config import SessionLocal
from app.middleware.authorize import authorize
from app.models.detail_person_duration import DetailPersonDuration
from app.models.person_duration import PersonDuration
from app.schemas.person_duration_schema import PersonDurationBaseCreate, PersonDurationBaseResponse, MessageResponsePersonDurationBase, PersonDurationWithDetailsResponse
from app.schemas.detail_person_duration_schema import DetailPersonDurationBaseResponse, EndTimeUpdateRequest, PersonDurationResponseUpdate
from app.controllers import detail_person_duration_controller, person_duration_controller

router = APIRouter(prefix="/person-durations", tags=["Person Duration"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Union[PersonDurationBaseResponse, MessageResponsePersonDurationBase])
def create_person_duration(
    person_duration_base: PersonDurationBaseCreate,
    _: None = Depends(authorize),
    db: Session = Depends(get_db)
):
    return person_duration_controller.create_person_duration(db, person_duration_base)

@router.post("/detail", response_model=DetailPersonDurationBaseResponse)
def create_detail_person_duration(
    _: None = Depends(authorize),
    nim: str = Form(...),
    name: str = Form(...),
    name_track_id: str = Form(...),
    image_file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    new_detail = detail_person_duration_controller.create_detail_person_duration(
        nim=nim,
        name=name,
        name_track_id=name_track_id,
        image_file=image_file,
        db=db
    )

    return DetailPersonDurationBaseResponse(
        person_duration_id=new_detail.person_duration_id,
        labeled_image=new_detail.labeled_image,
        nim=new_detail.nim,
        name=new_detail.name,
        name_track_id=new_detail.name_track_id,
        start_time=new_detail.start_time,
        end_time=new_detail.end_time,
    )

@router.patch("/detail/{track_name_id}", response_model=PersonDurationResponseUpdate)
def update_end_time(
    track_name_id: str,
    update_data: EndTimeUpdateRequest,
    _: None = Depends(authorize),
    db: Session = Depends(get_db)
):
    updated_person_duration = detail_person_duration_controller.update_end_time_by_track_name_id(
        track_name_id=track_name_id,
        end_time=update_data.end_time,
        db=db
    )

    return PersonDurationResponseUpdate(
        name_track_id=updated_person_duration.name_track_id,
        end_time=updated_person_duration.end_time,
    )

@router.get("/show-labeled-image")
async def show_labeled_image(
    filename: str,
    db: Session = Depends(get_db),
):
    return person_duration_controller.get_image(filename)

@router.get("/", response_model=List[PersonDurationWithDetailsResponse])
def get_person_durations(db: Session = Depends(get_db)):
    return person_duration_controller.get_all_person_durations_with_details(db)

@router.get("/{id}/details")
def get_person_duration_details(id: int, db: Session = Depends(get_db)):
    details = (
        db.query(DetailPersonDuration)
        .filter(DetailPersonDuration.person_duration_id == id)
        .order_by(desc(DetailPersonDuration.start_time))
        .all()
    )

    if not details:
        raise HTTPException(status_code=404, detail="Details not found for the given person_duration_id")

    return details