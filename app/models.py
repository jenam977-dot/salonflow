from pydantic import BaseModel, Field
from typing import Optional

class CustomerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    phone: str = Field(min_length=3, max_length=30)
    notes: Optional[str] = ""

class ServiceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    duration: int = Field(default=30, ge=5, le=480)
    price: float = Field(default=0, ge=0)

class AppointmentCreate(BaseModel):
    customer_id: int
    service_id: int
    appointment_date: str
    appointment_time: str
    notes: Optional[str] = ""

class StatusUpdate(BaseModel):
    status: str
