from __future__ import annotations

from carinsurance_api.db.base import Base, PKInt
from carinsurance_api.db.models.car import Car

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import List, Optional


class Owner(Base):
    __tablename__ = "owners"

    id: Mapped[int] = PKInt
    name: Mapped[str] = mapped_column(String(70), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, unique=True)
    cars: Mapped[List[Car]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan"
    )
