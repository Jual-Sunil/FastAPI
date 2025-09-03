import uuid
from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from backend.db.models.videos import Video
from backend.apps.v1.route_videos import format_duration
from backend.apis.v1.route_login import get_curr_user
from backend.db.models.users import User
from backend.db.session import get_db
from backend.apis.v1.route_chatbot import SemanticVideoSearch

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

# Register custom filter
templates.env.filters['format_duration'] = format_duration

@router.get('/chat')
def get_chat(request: Request, user: User = Depends(get_curr_user)):
    """Initialize chat interface"""
    try:
        context = {
            "request": request,
            "username": user.username,
            'prof_img': user.prof_img
        }
        
        return templates.TemplateResponse('components/chatbot.html', context=context)
        
    except Exception as e:
        print(f"Error in get_chat: {e}")
        raise HTTPException(status_code=500, detail="Failed to initialize chat")

@router.post("/chat/search", response_class=HTMLResponse)
async def description_semantic_search(
    request: Request,
    description: str = Form(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_curr_user)
):
    """Handle semantic search based on description"""
    try:
        if not description.strip():
            return JSONResponse({"error": "Empty description"}, status_code=400)
        
        # Get semantic search instance
        semantic_search = SemanticVideoSearch(db)
        
        # Find videos based on description
        videos = semantic_search.desc_based_vids(description, k=10)
        
        context = {
            'request': request,
            'videos': videos,
            'search_query': description,
            'search_type': 'description',
            "username": user.username,
            'prof_img': user.prof_img,
            'query': description
        }
        
        return templates.TemplateResponse("video_pages/search_results.html", context)
        
    except Exception as e:
        print(f"Error in description search: {e}")
        raise HTTPException(status_code=500, detail="Description search failed")

@router.get("/chat/suggestions")
async def get_suggestions(
    query: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_curr_user)
):
    """Get search suggestions based on partial query"""
    try:
        # Get a few quick suggestions based on existing tags and video titles
        suggestions = []
        
        # Search in tags
        tag_matches = db.query(Video.tags).filter(
            Video.tags.ilike(f"%{query}%")
        ).limit(5).all()
        
        for tag_row in tag_matches:
            if tag_row[0]:
                tags = [tag.strip() for tag in tag_row[0].split(",")]
                suggestions.extend([tag for tag in tags if query.lower() in tag.lower()])
        
        # Search in titles
        title_matches = db.query(Video.title).filter(
            Video.title.ilike(f"%{query}%")
        ).limit(5).all()
        
        suggestions.extend([title[0] for title in title_matches if title[0]])
        
        # Remove duplicates and limit results
        unique_suggestions = list(set(suggestions))[:8]
        
        return JSONResponse({"suggestions": unique_suggestions})
        
    except Exception as e:
        print(f"Error getting suggestions: {e}")
        return JSONResponse({"suggestions": []})

@router.post("/chat/refresh-vector-store")
async def refresh_vector_store(
    db: Session = Depends(get_db),
    user: User = Depends(get_curr_user)
):
    """Force refresh of the vector store to include new videos"""
    try:
        semantic_search = SemanticVideoSearch(db)
        semantic_search.refresh_vector_store()
        return JSONResponse({"message": "Vector store refreshed successfully"})
        
    except Exception as e:
        print(f"Error refreshing vector store: {e}")
        return JSONResponse({"error": "Failed to refresh vector store"}, status_code=500)