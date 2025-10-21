from carinsurance.db.base import Base, PKInt
from sqlalchemy import Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

class Car(Base):
    __tablename__ = "cars"

    id: Mapped[PKInt]
    vin: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    make: Mapped[str] = mapped_column(String(30), nullable=True)
    model: Mapped[str] = mapped_column(String(50), nullable=True)
    year_of_manufacture: Mapped[int] = mapped_column(Integer)

