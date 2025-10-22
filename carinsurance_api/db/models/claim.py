from carinsurance_api.db.base import Base, PKInt
from carinsurance_api.db.models.car import Car

from datetime import datetime, timezone, date

from sqlalchemy import Date, DateTime, ForeignKey, func, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Claim(Base):
    __tablename__ = "claims"

    id: Mapped[int] = PKInt
    claim_date: Mapped[date] = mapped_column(Date, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), server_default=func.now(), nullable=False)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"), nullable=False)
    car: Mapped[Car] = relationship(back_populates="claims")
