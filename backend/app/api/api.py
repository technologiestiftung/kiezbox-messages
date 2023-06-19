from fastapi import APIRouter

from app.api.endpoints import hello, messages

api_router = APIRouter()
api_router.include_router(hello.router, prefix="/hello_word", tags=["hello_world"])
api_router.include_router(messages.router, prefix="/messages", tags=["messages"])
