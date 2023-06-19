from datetime import datetime

from pydantic import BaseModel, Field


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
#    datetime: datetime = Field(default_factory=datetime.now) TODO: This line is throwing an error
    
    class Config:
        orm_mode = True   


# Properties to return to client
class Message(MessageInDBBase):
    pass


# Properties stored in DB
class MessageInDB(MessageInDBBase):
    pass
