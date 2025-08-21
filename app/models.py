from sqlalchemy import Column, Integer, String, Date
from app.database import Base

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    scraped_date = Column(Date, index=True) 
    name = Column(String(255))
    position = Column(String(100))
    club = Column(String(255))
    nationality = Column(String(255))
    age = Column(String(10))
    highest_value = Column(String(255))
    last_update = Column(String(255))
    market_value = Column(String(255))
