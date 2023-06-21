from sqlalchemy import Column, DateTime, Integer, String

from app.db.session import Base

class Message(Base):
    __tablename__ = "messages"
    
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, index=True)
    address: str = Column(String, index=True)
    problem: str = Column(String)
    number_affected_ppl: str = Column(Integer)
    timestamp = Column(DateTime)
