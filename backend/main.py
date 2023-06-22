import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.api import api_router
from app.core.config import settings
from app.db.session import engine, Base
from starlette.responses import FileResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_STR}/openapi.json"
)

out_folder = os.path.abspath("out")
extra_origin = os.getenv('UVICORN_HOST')

# Enable CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3030"
]
if extra_origin:
    origins.append(extra_origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_STR)

@app.get("/emergency")
def get_emergency():
    return FileResponse(os.path.join(out_folder, "emergency.html"))

@app.get("/inbox")
def get_inbox():
    return FileResponse(os.path.join(out_folder, "inbox.html"))

app.mount("/", StaticFiles(directory=out_folder, html=True), name="static")
