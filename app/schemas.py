from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class Depot(Base):
    __tablename__ = "depots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    location = Column(String(200), default="Non défini")
    floors_count = Column(Integer, default=1)
    racks_count = Column(Integer, default=1)
    slots_per_floor = Column(Integer, default=12)
    slot_width = Column(Float, default=1.0)
    slot_depth = Column(Float, default=1.0)
    description = Column(Text, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    sections = relationship("Section", back_populates="depot", cascade="all, delete-orphan")
    racks = relationship("Rack", back_populates="depot", cascade="all, delete-orphan")
    customers = relationship("Customer", back_populates="depot", cascade="all, delete-orphan")
    pallets = relationship("Pallet", back_populates="depot", cascade="all, delete-orphan")


class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    depot_id = Column(Integer, ForeignKey("depots.id"), nullable=False)
    name = Column(String(120), nullable=False)
    section_type = Column(String(60), default="carton")
    description = Column(Text, default="")
    is_active = Column(Boolean, default=True)

    depot = relationship("Depot", back_populates="sections")
    racks = relationship("Rack", back_populates="section", cascade="all, delete-orphan")
    pallets = relationship("Pallet", back_populates="section", cascade="all, delete-orphan")


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    depot_id = Column(Integer, ForeignKey("depots.id"), nullable=False)
    name = Column(String(120), nullable=False)
    company_name = Column(String(160), default="")
    contact = Column(String(160), default="")
    notes = Column(Text, default="")
    is_partner = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    depot = relationship("Depot", back_populates="customers")
    pallets = relationship("Pallet", back_populates="customer")


class Rack(Base):
    __tablename__ = "racks"

    id = Column(Integer, primary_key=True, index=True)
    depot_id = Column(Integer, ForeignKey("depots.id"), nullable=False)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=True)
    name = Column(String(120), nullable=False)
    floors_count = Column(Integer, default=3)
    slots_per_floor = Column(Integer, default=8)
    width = Column(Float, default=1.0)
    depth = Column(Float, default=1.2)
    is_active = Column(Boolean, default=True)
    status = Column(String(40), default="active")

    depot = relationship("Depot", back_populates="racks")
    section = relationship("Section", back_populates="racks")
    slots = relationship("Slot", back_populates="rack", cascade="all, delete-orphan")


class Slot(Base):
    __tablename__ = "slots"

    id = Column(Integer, primary_key=True, index=True)
    rack_id = Column(Integer, ForeignKey("racks.id"), nullable=False)
    floor_number = Column(Integer, default=1)
    slot_number = Column(Integer, default=1)
    status = Column(String(40), default="free")
    owner_type = Column(String(40), default="our")
    description = Column(Text, default="")

    rack = relationship("Rack", back_populates="slots")
    pallets = relationship("Pallet", back_populates="slot", cascade="all, delete-orphan")


class Pallet(Base):
    __tablename__ = "pallets"

    id = Column(Integer, primary_key=True, index=True)
    depot_id = Column(Integer, ForeignKey("depots.id"), nullable=False)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    slot_id = Column(Integer, ForeignKey("slots.id"), nullable=True)
    code = Column(String(80), nullable=False, unique=True)
    status = Column(String(40), default="stored")
    is_shared = Column(Boolean, default=False)
    weight = Column(Float, default=0.0)
    volume = Column(Float, default=0.0)
    notes = Column(Text, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    depot = relationship("Depot", back_populates="pallets")
    section = relationship("Section", back_populates="pallets")
    customer = relationship("Customer", back_populates="pallets")
    slot = relationship("Slot", back_populates="pallets")
