from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class Event(BaseModel):
    id: int
    # product_code: str
    date: date
    price: Decimal
