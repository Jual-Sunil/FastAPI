from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from backend.db.base_class import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable = False, unique = True)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    prof_img = Column(String, default = "")
    is_active = Column(Boolean, default=True)