from __future__ import annotations

from typing import List, Optional

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from carinsurance_api.db.base import Base, PKInt

# from carinsurance_api.db.models.claim import Claim
# from carinsurance_api.db.models.owner import Owner
# from carinsurance_api.db.models.policy import Policy


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[PKInt]
    vin: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    make: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    model: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    year_of_manufacture: Mapped[int] = mapped_column(Integer, nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("owners.id"), nullable=False)
    owner: Mapped["Owner"] = relationship(back_populates="cars")
    policies: Mapped[List["Policy"]] = relationship(
        back_populates="car",
        cascade="all, delete-orphan"
    )
    claims: Mapped[List["Claim"]] = relationship(
        back_populates="car",
        cascade="all, delete-orphan"
    )
