from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, mapped_column

from typing import Annotated


class Base(DeclarativeBase):
    """Declarative base class for SQLAlchemy models."""
    pass

PKInt = Annotated[int, mapped_column(Integer, primary_key=True, autoincrement=True)]
