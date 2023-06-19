from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.db.session import Base

class Message(Base):
    __tablename__ = "messages"
    
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, index=True)
    address: str = Column(String, index=True)
    problem: str = Column(String)
    number_affected_ppl: str = Column(Integer)
#    datetime: Column(Datetime) TODO: Pydantic is throwing an error in schema for the datetime field
