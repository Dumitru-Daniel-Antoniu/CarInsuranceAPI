from typing import Annotated

from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    """Declarative base class for SQLAlchemy models."""
    pass

PKInt = Annotated[int, mapped_column(Integer, primary_key=True, autoincrement=True)]
