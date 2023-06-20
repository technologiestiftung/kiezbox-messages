from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import crud_message
from app.schemas.message import Message, MessageCreate


router = APIRouter()


@router.get("/", response_model=List[Message])
async def read_messages(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve messages.
    """
    messages = crud_message.message.get_multi(db, skip=skip, limit=limit)
    return messages

@router.post("/", response_model=Message)
async def send_message(
    *,
    db: Session = Depends(deps.get_db),
    message_in:  MessageCreate,
) -> Any:
    """
    Send new message.
    """
    message = crud_message.message.create(db=db, obj_in=message_in)
    return message
