from datetime import date
from decimal import Decimal

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declarative_base,
    mapped_column,
    relationship,
)

Base: DeclarativeBase = declarative_base()


class DBCategory(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    events: Mapped[list["DBEvent"]] = relationship(back_populates="category")


class DBEvent(Base):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_code: Mapped[str] = mapped_column(unique=True)
    date: Mapped[date]
    price: Mapped[Decimal]
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    category: Mapped["DBCategory"] = relationship(back_populates="events")

    def __repr__(self):
        return (
            f"{self.id}: {self.product_code: 10} {self.category.name: 10} "
            f"{self.date}, ${self.price}"
        )
