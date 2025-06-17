from fastapi import APIRouter
from backend.apps.v1 import route_login
from backend.apps.v1 import route_videos
from backend.apps.v1 import route_register
from backend.apps.v1 import route_chatbot

app_router = APIRouter()

app_router.include_router(route_login.router, include_in_schema=False)
app_router.include_router(route_register.router, include_in_schema=False)
app_router.include_router(route_videos.router, include_in_schema=False)
app_router.include_router(route_chatbot.router, include_in_schema=False)