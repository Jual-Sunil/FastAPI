from fastapi import APIRouter
from backend.apis.v1 import route_user
from backend.apis.v1 import route_login
from backend.apis.v1 import route_scraping
from backend.apis.v1 import route_scheduling

api_router = APIRouter()

api_router.include_router(route_user.router, prefix="/user", tags=['user'])
api_router.include_router(route_login.router, prefix="/login", tags=['login'])
api_router.include_router(route_scraping.router, prefix="/scrape", tags=["scrape"])
api_router.include_router(route_scheduling.router, prefix="/schedule", tags=['schedule'])
