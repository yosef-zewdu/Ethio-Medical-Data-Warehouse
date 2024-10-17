from pydantic import BaseModel
from datetime import date

class Item(BaseModel):
    id: int
    channel_username: str 
    date: date 
    product: str
    price: int
    address: str

    class Config:
        from_attributes = True
