import os
from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Form  # type: ignore
from pydantic import BaseModel # type: ignore
from sqlalchemy.orm import Session # type: ignore
import models
from database import engine, SessionLocal
import secrets
import string
from datetime import datetime, timedelta
import pytz # type: ignore
from fastapi.responses import FileResponse # type: ignore

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class APIKeyBase(BaseModel):
    api_key: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def generate_api_key(length=32):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

@app.post("/generate-api-keys", tags=["Generate Api Key"])
async def generate_api_key_endpoint(db: Session = Depends(get_db)):
    random_api_key = await generate_api_key()  # Pastikan untuk menggunakan await
    db_api_key = models.APIKeys(api_key=random_api_key)
    db.add(db_api_key)
    db.commit()
    db.refresh(db_api_key)
    return db_api_key


@app.post("/person-duration", tags=["Person Duration"])
async def person_duration(api_key: str, file: UploadFile = File(...), nim: str = Form(...), name: str = Form(...), db: Session = Depends(get_db)):
    # Cek apakah api_key ada di database
    db_api_key = db.query(models.APIKeys).filter(models.APIKeys.api_key == api_key).first()
    
    if not db_api_key:
        raise HTTPException(status_code=403, detail="Invalid API key")

    # Cek apakah api_key sudah kadaluarsa
    current_time = datetime.now(pytz.timezone('Asia/Jakarta'))
    if current_time > db_api_key.expires_at:
        raise HTTPException(status_code=403, detail="API key has expired")

    # Buat nama file acak dengan ekstensi .jpg
    random_filename = f"{secrets.token_hex(16)}.jpg"  # Nama file acak dengan ekstensi .jpg

    # Simpan gambar ke server
    with open(f"images/{random_filename}", "wb") as image_file:
        image_file.write(await file.read())

    # Simpan informasi ke dalam database (labeled_image, nim, name)
    person_duration = models.PersonDurations(labeled_image=random_filename, nim=nim, name=name)
    db.add(person_duration)
    db.commit()
    db.refresh(person_duration)

    return {
        "filename": random_filename, 
        "nim": nim, 
        "name": name, 
        "start_time": person_duration.start_time
    }

@app.patch("/person-duration/{id}", tags=["Person Duration"])
async def update_person_duration_endtime(
    id: int, 
    api_key: str, 
    end_time: datetime,  # end_time sebagai datetime
    db: Session = Depends(get_db)
):
    # Cek apakah api_key ada di database
    db_api_key = db.query(models.APIKeys).filter(models.APIKeys.api_key == api_key).first()
    
    if not db_api_key:
        raise HTTPException(status_code=403, detail="Invalid API key")

    # Cek apakah api_key sudah kadaluarsa
    current_time = datetime.now(pytz.timezone('Asia/Jakarta'))
    if current_time > db_api_key.expires_at:
        raise HTTPException(status_code=403, detail="API key has expired")

    # Cari record PersonDurations berdasarkan id
    person_duration = db.query(models.PersonDurations).filter(models.PersonDurations.id == id).first()

    if not person_duration:
        raise HTTPException(status_code=404, detail="Person duration not found")

    # Set end_time dengan timezone Jakarta
    jakarta_tz = pytz.timezone('Asia/Jakarta')
    person_duration.end_time = end_time.astimezone(jakarta_tz)  # Pastikan end_time dalam timezone Jakarta

    db.commit()
    db.refresh(person_duration)

    return {
        "message": "End time updated successfully",
        "id": person_duration.id,
        "end_time": person_duration.end_time
    }

@app.get("/person-durations", tags=["Person Duration"])
async def get_all_person_durations(api_key: str, db: Session = Depends(get_db)):
    # Cek apakah api_key ada di database
    db_api_key = db.query(models.APIKeys).filter(models.APIKeys.api_key == api_key).first()
    
    if not db_api_key:
        raise HTTPException(status_code=403, detail="Invalid API key")

    # Cek apakah api_key sudah kadaluarsa
    current_time = datetime.now(pytz.timezone('Asia/Jakarta'))
    if current_time > db_api_key.expires_at:
        raise HTTPException(status_code=403, detail="API key has expired")

    # Ambil semua data dari tabel PersonDurations
    person_durations = db.query(models.PersonDurations).all()

    return {
        "person_durations": person_durations
    }

@app.get("/person-duration/{id}", tags=["Person Duration"])
async def get_person_duration_by_id(id: int, api_key: str, db: Session = Depends(get_db)):
    # Cek apakah api_key ada di database
    db_api_key = db.query(models.APIKeys).filter(models.APIKeys.api_key == api_key).first()
    
    if not db_api_key:
        raise HTTPException(status_code=403, detail="Invalid API key")

    # Cek apakah api_key sudah kadaluarsa
    current_time = datetime.now(pytz.timezone('Asia/Jakarta'))
    if current_time > db_api_key.expires_at:
        raise HTTPException(status_code=403, detail="API key has expired")

    # Cari record PersonDurations berdasarkan id
    person_duration = db.query(models.PersonDurations).filter(models.PersonDurations.id == id).first()

    if not person_duration:
        raise HTTPException(status_code=404, detail="Person duration not found")

    return {
        "person_duration": person_duration
    }

@app.get("/person-duration/show-labeled-image/", tags=["Person Duration"])
async def show_labeled_image(filename: str, api_key: str, db: Session = Depends(get_db)):
    # Cek apakah api_key ada di database
    db_api_key = db.query(models.APIKeys).filter(models.APIKeys.api_key == api_key).first()
    
    if not db_api_key:
        raise HTTPException(status_code=403, detail="Invalid API key")

    # Cek apakah api_key sudah kadaluarsa
    current_time = datetime.now(pytz.timezone('Asia/Jakarta'))
    if current_time > db_api_key.expires_at:
        raise HTTPException(status_code=403, detail="API key has expired")

    # Path file gambar
    file_path = os.path.join("images", filename)  # Sesuaikan dengan direktori yang benar

    # Cek file yang ada di direktori images
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path)


