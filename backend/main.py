import asyncio
from datetime import datetime
import json
import os
from typing import Annotated, List, Optional
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Form, Query, Request
from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sse_starlette import EventSourceResponse


extra_origin = os.getenv("UVICORN_HOST")

app = FastAPI(title="kiezbox-backend", openapi_url="/api/openapi.json")
app.mount("/static", StaticFiles(directory="static"), name="static")
# app.add_middleware(GZipMiddleware)  # enable middleware except for SSE
templates = Jinja2Templates(directory="templates")

# Enable CORS
origins = ["http://localhost", "http://localhost:8080", "http://localhost:3030"]
if extra_origin:
    origins.append(extra_origin)
    origins.append(f"{extra_origin}:8000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    address: str
    problem: str
    number_affected_ppl: str
    timestamp: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), index=True, server_default=func.now())
    )


connect_args = {"check_same_thread": False}
engine = create_engine("sqlite:///./backend.db", connect_args=connect_args)


def init_db():
    SQLModel.metadata.create_all(engine)


@app.on_event("startup")
def on_startup():
    init_db()


# Messages event generator TODO: Move to services directory
STREAM_DELAY = 5  # In seconds TODO: Maybe move to settings
# STREAM_TIMEOUT = 30000  # In milliseconds


async def messages_event_generator(
    request,
    skip: int = 0,
    limit: int = Query(default=100, le=100),
    as_html: bool = False,
):
    """
    Get status as an event generator.
    """
    previous_messages = []
    with Session(engine) as session:
        while True:
            # If client closes connection, stop sending events
            if await request.is_disconnected():
                break

            # Check for new messages and return them to client if any
            current_messages = session.exec(
                select(Message)
                .order_by(Message.timestamp.desc())
                .offset(skip)
                .limit(limit)
            ).all()
            if len(current_messages) > len(previous_messages):
                if as_html:
                    # Using the template is an advantage, but SSE can't handle encoded bytes
                    yield templates.TemplateResponse(
                        request=request,
                        name="inbox_content.html",
                        context={"messages": current_messages},
                    ).body.decode("utf-8")
                else:
                    yield json.dumps(jsonable_encoder(current_messages))

                previous_messages = current_messages

            await asyncio.sleep(STREAM_DELAY)


# Deprecated: old endpoint not used anymore
@app.get("/api/messages/stream", response_model=List[Message])
async def read_messages_stream(
    request: Request, skip: int = 0, limit: int = Query(default=100, le=100)
):
    """
    Retrieve messages and refresh with every new incoming message.
    """
    event_generator = messages_event_generator(request, skip=skip, limit=limit)

    return EventSourceResponse(event_generator, send_timeout=5)


# Deprecated: old endpoint not used anymore
@app.get("/api/messages/", response_model=List[Message])
async def read_messages(skip: int = 0, limit: int = Query(default=100, le=100)):
    with Session(engine) as session:
        messages = session.exec(
            select(Message).order_by(Message.timestamp.desc()).offset(skip).limit(limit)
        ).all()
        return messages


# Deprecated: old endpoint not used anymore
@app.post("/api/messages/", response_model=Message)
async def send_message_api(message: Message):
    with Session(engine) as session:
        session.add(message)
        session.commit()
        session.refresh(message)
        return message


@app.post("/messages", response_class=HTMLResponse)
async def send_message(
    name: Annotated[str, Form()],
    address: Annotated[str, Form()],
    problem: Annotated[str, Form()],
    number_affected_ppl: Annotated[int, Form()],
):
    message = Message(
        name=name,
        address=address,
        problem=problem,
        number_affected_ppl=number_affected_ppl,
    )
    with Session(engine) as session:
        session.add(message)
        session.commit()
        # session.refresh(message)

    return HTMLResponse(
        """
        <div class="grid w-full max-w-sm items-center gap-1.5 mt-6">
            <p>Dein Notruf wurde erfolgreich abgesetzt
            </p>
        </div>
        """
    )


@app.get("/emergency", response_class=HTMLResponse)
def get_emergency(request: Request):
    return templates.TemplateResponse(request=request, name="emergency.html")


@app.get("/inbox", response_class=HTMLResponse)
def get_inbox(request: Request):
    return templates.TemplateResponse(request=request, name="inbox.html")


@app.get("/inbox/stream", response_model=List[Message])
async def inbox_html_stream(
    request: Request, skip: int = 0, limit: int = Query(default=100, le=100)
):
    """
    Retrieve messages as HTML and refresh with every new incoming message.
    """
    event_generator = messages_event_generator(
        request, skip=skip, limit=limit, as_html=True
    )

    return EventSourceResponse(event_generator, send_timeout=5)


@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")
