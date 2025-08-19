from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DebtBase(BaseModel):
    item: str
    price: float
    description: Optional[str] = None

class DebtCreate(DebtBase):
    pass

class Debt(DebtBase):
    id: int
    date: datetime
    owner_id: int

    class Config:
        orm_mode = True

class PersonBase(BaseModel):
    name: str

class PersonCreate(PersonBase):
    pass

class Person(PersonBase):
    id: int
    debts: List[Debt] = []

    class Config:
        orm_mode = True

class TopDebtor(PersonBase):
    total_debt: float