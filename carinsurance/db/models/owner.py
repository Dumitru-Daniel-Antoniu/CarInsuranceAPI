from __future__ import annotations

from carinsurance.db.base import Base, PKInt
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional

class Owner(Base):
    __tablename__ = "owners"

    id: Mapped[PKInt]
    name: Mapped[str] = mapped_column(String(70), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, unique=True)
    cars: Mapped[List["Car"]] = relationship(
        back_populates="owner"
    )
