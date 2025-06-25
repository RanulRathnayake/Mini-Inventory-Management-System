from pydantic import BaseModel
from typing import Literal

class Product(BaseModel):
    product_id: str
    name: str
    stock_quantity: int
    min_threshold: int
    restock_quantity: int
    priority: Literal["high", "medium", "low"]
    category: Literal["high_volume", "low_volume"] = "low_volume"


class PurchaseRequest(BaseModel):
    quantity: int