from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class Item(Base):
    __tablename__ = "business_transformed"

    id = Column(Integer, primary_key=True, index=True)
    channel_username = Column(String, index=True)
    date = Column(DateTime, index=True)
    product = Column(String, index=True)
    price = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True)