from sqlalchemy.orm import Session
from db.models.users import User

def get_user_by_email(email : str, db : Session) -> User | None:
    return db.query(User).filter(User.email == email).first()
    