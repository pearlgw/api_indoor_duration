from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.controllers.api_key_controller import validate_api_key
from app.config.config import SessionLocal

security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Middleware untuk otorisasi
def authorize(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    api_key = credentials.credentials
    if not validate_api_key(api_key, db):
        raise HTTPException(status_code=401, detail="Invalid API key")
