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
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials # type: ignore

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
bearer_scheme = HTTPBearer()

class APIKeyBase(BaseModel):
    api_key: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
async def root_person_durations():
    return {"message" : "Selamat Datang di Api Person Durations"}

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

def verify_api_key(credentials: HTTPAuthorizationCredentials, db: Session):
    api_key = credentials.credentials  # Ambil API key dari header
    api_key_instance = db.query(models.APIKeys).filter(models.APIKeys.api_key == api_key).first()

    # Jika API key tidak ditemukan
    if not api_key_instance:
        raise HTTPException(status_code=403, detail="Invalid API key")

    # Ambil waktu saat ini di timezone Asia/Jakarta
    now = datetime.now(pytz.timezone('Asia/Jakarta'))

    # Jika API key sudah kadaluarsa
    if api_key_instance.expires_at < now:
        raise HTTPException(status_code=403, detail="API key has expired")

    return api_key_instance

@app.post("/person-duration", tags=["Person Duration"])
async def person_duration(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),  # Menggunakan Bearer token
    file: UploadFile = File(...),
    nim: str = Form(...),
    name: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        # Verifikasi API key dari Bearer token
        verify_api_key(credentials, db)

        # Buat nama file acak dengan ekstensi .jpg
        random_filename = f"{secrets.token_hex(16)}.jpg"

        # Simpan gambar ke server
        with open(f"images/{random_filename}", "wb") as image_file:
            image_file.write(await file.read())

        # Simpan informasi ke dalam database (labeled_image, nim, name)
        person_duration = models.PersonDurations(
            labeled_image=random_filename, 
            nim=nim, 
            name=name
        )
        db.add(person_duration)
        db.commit()
        db.refresh(person_duration)

        return {
            "filename": random_filename,
            "nim": nim,
            "name": name,
            "start_time": person_duration.start_time
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
    finally:
        db.close()

@app.patch("/person-duration/{id}", tags=["Person Duration"])
async def update_person_duration_endtime(
    id: int,
    end_time: str = Form(...),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    try:
        # Verifikasi API key dari Bearer token
        verify_api_key(credentials, db)

        # Cari record PersonDurations berdasarkan id
        person_duration = db.query(models.PersonDurations).filter(models.PersonDurations.id == id).first()

        if not person_duration:
            raise HTTPException(status_code=404, detail="Person duration not found")

        # Konversi string end_time menjadi datetime
        jakarta_tz = pytz.timezone('Asia/Jakarta')
        end_time_dt = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S")  # Pastikan format sesuai
        person_duration.end_time = end_time_dt.astimezone(jakarta_tz)  # Pastikan end_time dalam timezone Jakarta

        db.commit()
        db.refresh(person_duration)

        return {
            "message": "End time updated successfully",
            "id": person_duration.id,
            "end_time": person_duration.end_time
        }

    except HTTPException as e:
        raise e
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use 'YYYY-MM-DDTHH:MM:SS'")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating person duration: {str(e)}")
    finally:
        db.close()

@app.get("/person-durations", tags=["Person Duration"])
async def get_all_person_durations(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),  # Menggunakan Bearer token
    db: Session = Depends(get_db)
):
    try:
        # Verifikasi API key dari Bearer token
        api_key_instance = verify_api_key(credentials, db)

        # Ambil semua data dari tabel PersonDurations
        person_durations = db.query(models.PersonDurations).all()

        return {
            "person_durations": person_durations  # Mengembalikan daftar person_durations
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving person durations: {str(e)}")
    finally:
        db.close()

@app.get("/person-duration/{id}", tags=["Person Duration"])
async def get_person_duration_by_id(
    id: int,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),  # Menggunakan Bearer token
    db: Session = Depends(get_db)
):
    try:
        # Verifikasi API key dari Bearer token
        api_key_instance = verify_api_key(credentials, db)

        # Cari record PersonDurations berdasarkan id
        person_duration = db.query(models.PersonDurations).filter(models.PersonDurations.id == id).first()

        if not person_duration:
            raise HTTPException(status_code=404, detail="Person duration not found")

        return {
            "person_duration": person_duration  # Mengembalikan detail person_duration
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving person duration: {str(e)}")
    finally:
        db.close()

@app.get("/person-duration/show-labeled-image/", tags=["Person Duration"])
async def show_labeled_image(
    filename: str,
    db: Session = Depends(get_db)
):
    try:
        # Path file gambar
        file_path = os.path.join("images", filename)  # Sesuaikan dengan direktori yang benar

        # Cek file yang ada di direktori images
        if not os.path.isfile(file_path):
            raise HTTPException(status_code=404, detail="File not found")

        return FileResponse(file_path)  # Mengembalikan file gambar sebagai respons

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving image: {str(e)}")