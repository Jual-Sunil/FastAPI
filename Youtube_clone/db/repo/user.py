from sqlalchemy.orm import Session
from schemas.user import UserCreate
from db.models.users import User
from core.hashing import Hasher

def create_user(user : UserCreate, db : Session):
    user =  User(
        username = user.username,
        email = user.email,
        password = Hasher.get_pass_hash(user.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user