from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


# Shared properties
class MessageBase(BaseModel):
    name: str
    address: str
    problem: str
    number_affected_ppl: int


# Properties to receive on message creation
class MessageCreate(MessageBase):
    pass


# Properties to receive on message update
class MessageUpdate(MessageBase):
    pass


# Properties shared by models stored in DB
class MessageInDBBase(MessageBase):
    id: int
    timestamp: datetime

    @validator("timestamp", pre=True, always=True)
    def set_timestamp(cls, v):
        return v or datetime.now()

    class Config:
        orm_mode = True


# Properties to return to client
class Message(MessageInDBBase):
    pass


# Properties stored in DB
class MessageInDB(MessageInDBBase):
    pass
