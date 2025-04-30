from fastapi import APIRouter
from apps.v1 import route_login

app_router = APIRouter()

app_router.include_router(route_login.router, include_in_schema=False)