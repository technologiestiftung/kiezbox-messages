from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.schemas.message import Message, MessageCreate
from app.api import deps
from app.crud import crud_message


router = APIRouter()

# TODO: Dummy response, delete later
dummy_msg_1 = {
    "id": 0,
    "name": "Juanito",
    "address": "Grunewaldstrasse 61",
    "problem": "We ran out of Apfelschorle",
    "number_affected_ppl": 10,
    "datetime": "19.06.2023"
}

dummy_msg_2 = {
    "id": 1,
    "name": "Pepito",
    "address": "Grunewaldstrasse 61",
    "problem": "The coffee machine broke",
    "number_affected_ppl": 10,
    "datetime": "19.06.2023"
}

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
