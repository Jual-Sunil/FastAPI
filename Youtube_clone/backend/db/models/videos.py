from datetime import datetime
from sqlalchemy import Column, Integer, Text, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.db.base_class import Base

class Video(Base):
    __tablename__ = "videos"
    id = Column(String, primary_key = True)    
    title = Column(String, nullable=False)
    desc = Column(Text, nullable = False)
    video_url = Column(String(500), nullable = False)
    thumbnail_url = Column(String(500))
    source = Column(String, default = "youtube") # youtube, vimeo or upload
    upload_type = Column(String, default = "scraped") # or upload
    creator_id = Column(String, nullable=True)
    creator_name = Column(String(100))
    created_at = Column(DateTime, default= datetime.now)
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    tags = Column(String)
    duration = Column(String)
    q_tag = Column(String)
    is_active = Column(Boolean, default=True)