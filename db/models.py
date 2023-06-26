"""
Definitions of DB tables.
Car to Reservation has one-to-many relationship (one car can have multiple reservations)
"""
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Car(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True)
    uid = Column(String(10))  # C123456789 - we assume 9-digit id (i.e. max 999999999 cars)
    maker = Column(String(50))
    model = Column(String(50))
    reservations = relationship("Reservation", back_populates="car")


class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey("cars.id"))
    car = relationship("Car", back_populates="reservations")
    start_timestamp = Column(Integer)
    end_timestamp = Column(Integer)
