from typing import Any, List

import asyncio
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from sse_starlette.sse import EventSourceResponse

from app.api import deps
from app.crud import crud_message
from app.schemas.message import Message, MessageCreate


router = APIRouter()

# Messages event generator TODO: Move to services directory
STREAM_DELAY = 5  # In seconds TODO: Maybe move to settings
STREAM_TIMEOUT = 30000  # In milliseconds


async def messages_event_generator(
    request,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100):
    """
    Get status as an event generator.
    """
    previous_messages = []
    while True:
        # If client closes connection, stop sending events
        if await request.is_disconnected():
            break

        # Check for new messages and return them to client if any
        # TODO: Convert response to a readable format for frontend
        current_messages = crud_message.message.get_multi(db, skip=skip, limit=limit)
        if len(current_messages) > len(previous_messages):
            yield {
                "event": "update",
                "retry": STREAM_TIMEOUT,
                "data": current_messages
            }

            previous_messages = current_messages

        await asyncio.sleep(STREAM_DELAY)


@router.get("/stream", response_model=List[Message])
async def read_messages_stream(
    request: Request,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Retrieve messages and refresh with every new incoming message.
    """
    event_generator = messages_event_generator(request, db, skip=skip, limit=limit)
    return EventSourceResponse(event_generator)


@router.get("/",
            response_model=List[Message])
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


@router.post("/",
             response_model=Message)
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
