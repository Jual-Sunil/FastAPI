from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from dateutil import parser

from db.models.videos import Video
from db.session import get_db
from core.config import settings

import random, requests, isodate

router = APIRouter()

def search_youtube(api_key, query, max_results=10):
    url = "https://www.googleapis.com/youtube/v3/search"
    parameters = {
        'key' : api_key,
        'q' : query,
        'part' : 'snippet',
        'type' : 'video',
        'maxResults' : max_results
    }
    response = requests.get(url, params=parameters)
    return response.json().get('items',[])

def video_details(api_key, video_ids):
    url = "https://www.googleapis.com/youtube/v3/videos"
    parameters = {
        'key' : api_key,
        'id' : ",".join(video_ids),
        'part' : "snippet, contentDetails, statistics, id, channelTitle"
    }
    response = requests.get(url, params=parameters)
    return response.json().get('items', [])

def convert_vid_duration(iso_duration):
    try :
        duration = isodate.parse_duration(iso_duration)
        return str(duration)
    except :
        return ''

def map_videos_to_db(video):
    snippets = video['snippet']
    content_dets = video['contentDetails']
    stats = video.get("statistics", {})
    vid_id = video['id']
    return Video(
        id = vid_id,
        title = snippets['title'],
        desc = snippets['description'],
        video_url = f"https://www.youtube.com/watch?v={vid_id}",
        thumbnail_url = snippets['thumbnails']['high']['url'],
        source = 'youtube',
        upload_type = 'scraped',
        creator_id = snippets['channelId'],
        creator_name = video['channelTitle'],
        created_at = parser.parse(snippets['publishedAt']),
        views = int(stats.get('viewCount', 0)),
        likes = int(stats.get('likeCount', 0)),
        tags = ", ".join(snippets.get('tags', [])),
        duration = convert_vid_duration(content_dets['duration']),
        is_active = True
    )

@router.post('/videos')
def scrape_save_videos(db : Session = Depends(get_db)):
    query = random.choice(settings.QUERY_KEYWORD_LIST)
    search_videos = search_youtube(settings.YOUTUBE_DATAKEY, query=query, max_results=10)
    video_ids = [item["id"]['videoId'] for item in search_videos if "videoId" in item['id']]
    detailed_videos = video_details(settings.YOUTUBE_DATAKEY, video_ids)

    for video in detailed_videos:
        db_video = map_videos_to_db(video)
        #skip func
        existing_vid = db.query(Video).filter(Video.video_url == db_video.video_url).first()
        if not existing_vid:
            db.add(db_video)
            db.commit()
            db.refresh(db_video)
    return {"message" : f"Added {len(detailed_videos)} videos from keyword: {query}"}

