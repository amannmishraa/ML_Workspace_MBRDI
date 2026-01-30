from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    predicted_price = Column(Float)
    sold_within_week = Column(Integer)

    condition = Column(String)
    location_type = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)
