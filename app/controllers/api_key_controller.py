from app.models.api_key import ApiKey
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import uuid
from fastapi import HTTPException

def generate_api_key(db: Session):
    new_key = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(days=365)
    api_key_entry = ApiKey(api_key=new_key, expires_at=expires_at)
    db.add(api_key_entry)
    db.commit()
    db.refresh(api_key_entry)
    return api_key_entry

def validate_api_key(api_key: str, db: Session):
    key_entry = db.query(ApiKey).filter(ApiKey.api_key == api_key).first()
    if not key_entry or key_entry.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Invalid or expired API key")
    return key_entry
