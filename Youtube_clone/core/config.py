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
    POSTGRES_USER: str = os.getenv("USER")
    POSTGRES_PASSWORD: str = os.getenv("PASSWORD")
    POSTGRES_SERVER: str = os.getenv("SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("PORT",5432)
    POSTGRES_DB: str = os.getenv("Database")
    DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    # JSON web token creation (JWT)
    KEY : str = os.getenv("SECRET_KEY")
    ALGORITHM : str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    #Google auth and login settings
    GOOGLE_CLIENT_ID : str = os.getenv("GOOGLE_CLIENTID")
    GOOGLE_CLIENT_SECRET : str = os.getenv("GOOGLE_CLIENTSECRET")
    #Youtube API settings
    YOUTUBE_DATAKEY : str = os.getenv("YOUTUBE_DATA_KEY")
    YOUTUBE_FETCHURL = str = os.getenv("YOUTUBE_FETCH_URL")
    QUERY_KEYWORD_LIST = ["music", "technology", "news", "sports", "travel", "education", "comedy", "movies", "science",
                        "gaming", "vlogs", "fitness", "health", "finance", "motivation", "art", "photography", "cooking",
                        "DIY", "history", "space", "nature", "animals", "interviews", "tutorials", "makeup", "fashion",
                        "cars", "motorcycles", "architecture", "food", "recipes", "animation", "reviews", "books",
                        "productivity", "coding", "startups", "culture", "documentary", "psychology", "languages", "dance",
                        "instrumental", "spirituality", "investing", "home decor", "martial arts", "parenting", "challenges"]
settings = Settings()