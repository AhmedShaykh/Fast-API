from pydantic import BaseModel;
from typing import Optional;

class ProductSchema(BaseModel):
    title: str;
    desc: str;
    price: float;

class UpdateProductSchema(BaseModel):
    title: Optional[str] = None;
    desc: Optional[str] = None;
    price: Optional[float] = None;