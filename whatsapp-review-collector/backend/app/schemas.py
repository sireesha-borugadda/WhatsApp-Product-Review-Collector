from pydantic import BaseModel
from datetime import datetime

class ReviewCreate(BaseModel):
    contact_number: str
    user_name: str
    product_name: str
    product_review: str

class ReviewOut(BaseModel):
    id: int
    contact_number: str
    user_name: str
    product_name: str
    product_review: str
    created_at: datetime

    class Config:
        orm_mode = True
