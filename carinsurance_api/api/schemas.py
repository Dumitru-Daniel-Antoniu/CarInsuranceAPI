from datetime import date, datetime
from typing import Optional

from pydantic import (BaseModel, Field, StrictFloat, StrictInt, StrictStr,
                      field_validator)


class OwnerSchema(BaseModel):
    id: Optional[StrictInt] = None
    name: StrictStr
    email: Optional[StrictStr] = None

    class Config:
        from_attributes = True
        populate_by_name = True


class CarSchema(BaseModel):
    id: Optional[StrictInt] = None
    vin: StrictStr
    make: Optional[StrictStr] = None
    model: Optional[StrictStr] = None
    year_of_manufacture: StrictInt = Field(alias="yearOfManufacture")
    owner_id: StrictInt = Field(alias="ownerId")

    class Config:
        from_attributes = True
        populate_by_name = True


class PolicySchema(BaseModel):
    id: Optional[StrictInt] = None
    provider: Optional[StrictStr] = None
    start_date: date = Field(alias="startDate")
    end_date: date = Field(alias="endDate")
    logged_expiry_at: Optional[datetime] = Field(default=None, alias="loggedExpiryAt")
    car_id: StrictInt = Field(alias="carId")

    @field_validator("start_date", "end_date")
    def date_range_guard(cls, v):
        if not (1900 <= v.year <= 2100):
            raise ValueError("Date must be between 1900 and 2100.")
        return v

    @field_validator("end_date")
    def end_after_start(cls, v, info):
        start = info.data.get("start_date")
        if start and v < start:
            raise ValueError("End date must be after or equal to start date.")
        return v

    class Config:
        from_attributes = True
        populate_by_name = True


class ClaimSchema(BaseModel):
    id: Optional[StrictInt] = None
    claim_date: date = Field(alias="claimDate")
    description: StrictStr
    amount: StrictFloat
    created_at: Optional[datetime] = Field(default=None, alias="createdAt")
    car_id: StrictInt = Field(alias="carId")

    @field_validator("claim_date")
    def date_range_guard(cls, v):
        if not (date(1900, 1, 1) <= v <= date.today()):
            raise ValueError("Claim date must be between 1900 and current day.")
        return v

    @field_validator("amount")
    def positive_amount(cls, v):
        if v <= 0:
            raise ValueError("Amount must be positive.")
        return v

    @field_validator("amount")
    def reasonable_amount(cls, v):
        if v >= 20000:
            raise ValueError("Amount is too big.")
        return v

    class Config:
        from_attributes = True
        populate_by_name = True
