from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Client(Base):
    __tablename__ = "clients"

    active = Column(Boolean, default=True)
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    image = Column(String, nullable=True)

    orders = relationship("Order", back_populates="client")

class Instrument(Base):
    __tablename__ = "instruments"
    
    active = Column(Boolean, default=True)
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    brand = Column(String)
    price = Column(Float)
    stock = Column(Integer)
    image = Column(String, nullable=True)

class Order(Base):
    __tablename__ = "orders"
    
    active = Column(Boolean, default=True)
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    instrument_id = Column(Integer, ForeignKey("instruments.id"))
    quantity = Column(Integer)
    total = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    client = relationship("Client", back_populates="orders")
    instrument = relationship("Instrument")
