from pydantic import BaseModel, Field
from typing import List, Dict

class Chatbot_input(BaseModel):
    message : str
    role : str = 'user'
    conversation_id : str

class Message(BaseModel):
    role: str
    content: str

class Conversations(BaseModel):
    messages : List[Message] = Field(default_factory=list)

