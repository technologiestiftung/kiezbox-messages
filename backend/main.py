import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.api import api_router
from app.core.config import settings
from app.db.session import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_STR}/openapi.json")

#subapp = FastAPI(
#    title="api", openapi_url=f"{settings.API_STR}/openapi.json"
#)
#app.mount("/api", subapp)
out_folder = os.path.abspath("out")


# Enable CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3030"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_STR)
app.mount("/", StaticFiles(directory=out_folder, html=True), name="out")
