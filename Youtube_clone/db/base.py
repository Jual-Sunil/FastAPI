from db.base_class import Base
from db.models.users import User
from db.models.videos import Video
from sqlalchemy.orm import relationship

User.videos = relationship("Video", back_populates = 'creator')
Video.creator = relationship("User", back_populates = 'videos')