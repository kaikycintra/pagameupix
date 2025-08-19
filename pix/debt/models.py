from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base

class Person(Base):
    __tablename__ = "people"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    debts = relationship("Debt", back_populates="owner")

class Debt(Base):
    __tablename__ = "debts"
    id = Column(Integer, primary_key=True, index=True)
    item = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float)
    date = Column(DateTime, default=datetime.now(timezone.utc))
    owner_id = Column(Integer, ForeignKey("people.id"))
    owner = relationship("Person", back_populates="debts")