from fastapi import FastAPI

from app.api.api import api_router
from app.core.config import settings
from app import crud, models, schemas
from app.db.session import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_STR}/openapi.json"
)

app.include_router(api_router, prefix=settings.API_STR)
