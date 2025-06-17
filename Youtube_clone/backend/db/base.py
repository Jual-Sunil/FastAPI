from backend.db.base_class import Base
from backend.db.models.users import User
from backend.db.models.videos import Video

# User.videos = relationship("Video", back_populates = 'creator')
# Video.creator = relationship("User", back_populates = 'videos')