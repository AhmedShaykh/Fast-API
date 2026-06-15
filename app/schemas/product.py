from pydantic import BaseModel;
from typing import Optional;

class ProductSchema(BaseModel):
    title: str;
    desc: str;
    complete: bool = False;

class UpdateProductSchema(BaseModel):
    title: Optional[str] = None;
    desc: Optional[str] = None;
    complete: Optional[bool] = None;
