from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ClientBase(BaseModel):
    name: str
    email: str
    phone: str

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: int
    image: Optional[str] = None
    class Config:
        orm_mode = True

class InstrumentBase(BaseModel):
    name: str
    brand: str
    price: float
    stock: int

class InstrumentCreate(InstrumentBase):
    pass

class Instrument(InstrumentBase):
    id: int
    image: Optional[str] = None
    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    client_id: int
    instrument_id: int
    quantity: int

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    total: float
    created_at: datetime
    class Config:
        orm_mode = True
