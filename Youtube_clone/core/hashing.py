from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto") 

class Hasher:
    @staticmethod
    def verify_pass(plain_pass, hashed_pass):
        return pwd_context.verify(plain_pass, hashed_pass)
    
    @staticmethod
    def get_pass_hash(password):
        return pwd_context.hash(password)