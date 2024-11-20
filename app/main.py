from fastapi import Depends, FastAPI
from app.controllers import api_key_controller
from app.routes import person_duration_routes
from app.config.config import Base, engine
from app.schemas.api_key_schema import ApiKeyResponse
from app.config.config import SessionLocal
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Welcome to v2 api dinus indoor duration "}

@app.post("/generate-api-key", response_model=ApiKeyResponse, tags=["Auth"])
def generate_key(db: Session = Depends(get_db)):
    api_key = api_key_controller.generate_api_key(db)
    return api_key

app.include_router(person_duration_routes.router)