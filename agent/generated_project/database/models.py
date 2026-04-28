from sqlalchemy import Column, Integer, String
from database.db import Base   # 🔥 IMPORTANT FIX

class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    content = Column(String)