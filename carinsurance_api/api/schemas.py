from datetime import date, datetime
from typing import Optional

from pydantic import (BaseModel, Field, StrictFloat, StrictInt, StrictStr,
                      field_validator)


class OwnerSchema(BaseModel):
    id: int
    name: StrictStr
    email: Optional[StrictStr]

    class Config:
        from_attributes = True
        populate_by_name = True


class CarSchema(BaseModel):
    id: int
    vin: StrictStr
    make: Optional[StrictStr]
    model: Optional[StrictStr]
    year_of_manufacture: StrictInt = Field(alias="yearOfManufacture")
    owner_id: StrictInt = Field(alias="ownerId")

    class Config:
        from_attributes = True
        populate_by_name = True


class PolicySchema(BaseModel):
    id: int
    provider: Optional[StrictStr]
    start_date: date = Field(alias="startDate")
    end_date: date = Field(alias="endDate")
    logged_expiry_at: Optional[datetime] = Field(alias="loggedExpiryAt")
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
    id: int
    claim_date: date = Field(alias="claimDate")
    description: StrictStr
    amount: StrictFloat
    created_at: datetime = Field(alias="createdAt")
    car_id: StrictInt = Field(alias="carId")

    @field_validator("claim_date")
    def date_range_guard(cls, v):
        current_year = datetime.now().year
        if not (1900 <= v.year <= current_year):
            raise ValueError("Claim date must be between 1900 and current year.")
        return v

    @field_validator("amount")
    def positive_amount(cls, v):
        if v <= 0:
            raise ValueError("Amount must be positive.")
        return v

    class Config:
        from_attributes = True
        populate_by_name = True
