from sqlalchemy.orm import Session
from backend.schemas.user import UserCreate
from backend.db.models.users import User
from backend.core.hashing import Hasher

def create_new_user(user : UserCreate, db : Session):
    user =  User(
        username = user.username,
        email = user.email,
        password = Hasher.get_pass_hash(user.password),
        prof_img = user.prof_img
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user