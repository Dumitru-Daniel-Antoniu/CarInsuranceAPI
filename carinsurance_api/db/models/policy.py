from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from sqlalchemy import Date, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from carinsurance_api.db.base import Base, PKInt

# from carinsurance_api.db.models.car import Car


class Policy(Base):
    __tablename__ = "policies"

    id: Mapped[PKInt]
    provider: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    logged_expiry_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"), nullable=False)
    car: Mapped["Car"] = relationship(back_populates="policies")
