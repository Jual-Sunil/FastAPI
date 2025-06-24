import uuid
import random
from typing import List
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import or_

from backend.db.models.videos import Video
from backend.apps.v1.route_videos import format_duration
from backend.apis.v1.route_login import get_curr_user
from backend.db.models.users import User
from backend.db.session import get_db
from backend.apis.v1.route_chatbot import query_cohere_api, convo_storage, select_tags
from backend.schemas.chatbot import Conversations, Message

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

templates.env.filters['format_duration'] = format_duration

@router.get('/chat')
def get_chat(request: Request, conversation_id: str = None, user : User = Depends(get_curr_user)):
    if not conversation_id:
        conversation_id = str(uuid.uuid4())
        convo_storage[conversation_id] = Conversations()
        convo_storage[conversation_id].messages.append({
             "role": "assistant",
            "content": "How may I assist you today? <br> 1. Find videos based on your preferred tags. <br> 2. Find videos based on your description."
        })

    convo = convo_storage.get(conversation_id)
    context = {
        "request" : request, 
        "conversation_id" : conversation_id, 
        "messages" : convo.messages,
        "username" : user.username,
        "prof_img" : user.prof_img
        }
    
    return templates.TemplateResponse('components/chatbot.html',context=context)


@router.post('/chat')
def chat(request : Request, conversation_id : str = Form(...), message : str = Form(...), db : Session = Depends(get_db), user : User = Depends(get_curr_user)):
    convo = convo_storage.get(conversation_id)

    if not convo.messages:
        initial_prompt = "How may I assist you today? <br>1. Find videos based on your preferred tags.<br> 2. Find videos based on your description."
        convo.messages.append(Message(role="assistant", content=initial_prompt))
        return {"response" : initial_prompt}
    user_msg = message.strip()

    #default handle
    response = ""
    context = {'request' : request, 
               'conversation_id' : conversation_id, 
               'messages' : convo.messages,
               "username" : user.username,
               "prof_img" : user.prof_img
        }


    if user_msg == "1":
        response = "Great! Please select one or more tags you're interested in."
        convo.messages.append(Message(role="assistant", content=response))
        tags = select_tags(db)
        print("Tags:",tags)
        context['tags'] = tags
        return templates.TemplateResponse("components/chatbot.html", context=context)
    
    elif user_msg == "2":
        response = "Okay! Please describe the kind of video you're looking for."
        convo.messages.append(Message(role="assistant", content=response))
        return templates.TemplateResponse("components/chatbot.html", context=context )
    else:
        response = query_cohere_api(convo)
        if not response.strip():
            response = "Sorry, I couldn't process your request"

    AI_msg = Message(role='assistant', content=response)
    convo.messages.append(Message(role='User',content=user_msg))
    convo.messages.append(AI_msg)

    context = {'request' : request, 'conversation_id' : conversation_id, 'messages' : convo.messages, 'tags' : tags}
    return templates.TemplateResponse('components/chatbot.html',context=context)

@router.post("/chat/tag-res", response_class=HTMLResponse)
async def tags_result(request : Request, selected_tags : List[str] = Form(...), db : Session = Depends(get_db), user : User = Depends(get_curr_user) ):
    form = await request.form()
    videos = db.query(Video).filter(
        or_(*[Video.tags.ilike(f"%{tag}%") for tag in selected_tags])
    ).all()
    final_tags = form.getlist("selected_tags")
    context = {'request' : request, 
               'videos' : videos, 
               'tags' : final_tags,
               "username" : user.username,
               "prof_img" : user.prof_img
        }

    return templates.TemplateResponse("video_pages/tag_res.html", context=context)
