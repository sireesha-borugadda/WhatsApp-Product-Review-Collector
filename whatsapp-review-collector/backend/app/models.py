from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from .db import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    contact_number = Column(String, index=True)
    user_name = Column(String, index=True)
    product_name = Column(String, index=True)
    product_review = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
