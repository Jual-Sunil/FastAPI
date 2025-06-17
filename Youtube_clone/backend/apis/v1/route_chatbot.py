import cohere
import random
from typing import Dict
from sqlalchemy.orm import Session

from backend.core.config import settings
from backend.schemas.chatbot import Conversations
from backend.db.models.videos import Video
from backend.db.session import get_db

client = cohere.Client(api_key=settings.COHERE_APIKEY)
convo_storage : Dict[str, Conversations] = {}

def query_cohere_api(chat : Conversations) -> str:
    try:
        history = []
        for msg in chat.messages[:-1]:
            if msg.role == "user":
                history.append({'role' : 'USER', "message" : msg.content})
            elif msg.role == "assistant":
                history.append({'role' : 'CHATBOT', "message" : msg.content})
        
        if chat.messages:
            last_msg = chat.messages[-1].content
        else:
            last_msg = ""
        
        response = client.chat(
            message=last_msg,
            chat_history=history,
            model="command-r-plus",
            temperature=0.9,
        )
        return response.text
    
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while querying"

def select_tags(db: Session) -> str:
    all_tags = db.query(Video.tags).distinct().all()
    tag_set = set()

    for row in all_tags:
        tag_str = row[0]
        if tag_str:
            tag_set.update(tag.strip() for tag in tag_str.split(",") if tag.strip())

    rnd_tags = random.sample(tag_set, min(len(tag_set),20))
    return rnd_tags


