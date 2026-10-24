from __future__ import annotations

from typing import Optional, Literal

from pydantic import BaseModel, Field


StatusEnum = Literal["free", "occupied_our", "occupied_customer", "shared", "reserved"]
OwnerTypeEnum = Literal["our", "customer", "shared"]


class DepotBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    location: str = "Non défini"
    floors_count: int = 2
    racks_count: int = 4
    slots_per_floor: int = 12
    slot_width: float = 1.0
    slot_depth: float = 1.2
    description: str = ""


class DepotCreate(DepotBase):
    pass


class DepotUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    floors_count: Optional[int] = None
    racks_count: Optional[int] = None
    slots_per_floor: Optional[int] = None
    slot_width: Optional[float] = None
    slot_depth: Optional[float] = None
    description: Optional[str] = None


class SectionBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    section_type: str = "carton"
    description: str = ""
    is_active: bool = True


class SectionCreate(SectionBase):
    depot_id: int


class CustomerBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    company_name: str = ""
    contact: str = ""
    notes: str = ""
    is_partner: bool = False


class CustomerCreate(CustomerBase):
    depot_id: int


class RackBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    floors_count: int = 3
    slots_per_floor: int = 8
    width: float = 1.0
    depth: float = 1.2
    is_active: bool = True
    status: str = "active"


class RackCreate(RackBase):
    depot_id: int
    section_id: Optional[int] = None


class SlotBase(BaseModel):
    floor_number: int = 1
    slot_number: int = 1
    status: StatusEnum = "free"
    owner_type: OwnerTypeEnum = "our"
    description: str = ""


class SlotCreate(SlotBase):
    rack_id: int


class PalletBase(BaseModel):
    code: str = Field(..., min_length=2, max_length=80)
    weight: float = 0.0
    volume: float = 0.0
    notes: str = ""
    is_shared: bool = False
    status: str = "stored"


class PalletCreate(PalletBase):
    depot_id: int
    section_id: Optional[int] = None
    customer_id: Optional[int] = None
    slot_id: Optional[int] = None


class PalletStatusUpdate(BaseModel):
    status: str = "stored"
    slot_id: Optional[int] = None
    customer_id: Optional[int] = None
    is_shared: Optional[bool] = None


class DashboardSummary(BaseModel):
    depots_count: int
    racks_count: int
    sections_count: int
    customers_count: int
    pallets_count: int
    free_slots: int
    occupied_our: int
    occupied_customer: int
    shared_slots: int
