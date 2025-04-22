import os
from dotenv import load_dotenv
from pathlib import Path
env_path = Path(".") / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    #Basic project details
    PROJECT_TITLE = "You clone"
    PROJECT_VERSION = '0.1.0'
    #Database details
    POSTGRES_USER: str = os.getenv("SER")
    POSTGRES_PASSWORD: str = os.getenv("PASSWORD")
    POSTGRES_SERVER: str = os.getenv("SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("PORT",5432)
    POSTGRES_DB: str = os.getenv("Database")
    DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    # JSON web token creation (JWT)
    KEY : str = os.getenv("SECRET_KEY")
    ALGORITHM : str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()