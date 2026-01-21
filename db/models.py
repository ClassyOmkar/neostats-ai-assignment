from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    bookings = relationship("Booking", back_populates="customer")

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    booking_type = Column(String, nullable=False) # e.g., Consultation, Cleaning
    date_time = Column(DateTime, nullable=False)
    status = Column(String, default="Confirmed")
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="bookings")
