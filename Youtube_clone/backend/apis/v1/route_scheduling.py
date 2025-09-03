from fastapi import APIRouter, Depends
from apscheduler.schedulers.background import BackgroundScheduler
from time import sleep
from sqlalchemy.orm import Session

from backend.db.session import get_db, SESSIONLOCAL
from backend.apis.v1.route_scraping import scrape_save_videos

router = APIRouter()
scheduler = BackgroundScheduler()

def scheduled_scrape():
    db: Session = SESSIONLOCAL()
    try:
        scrape_save_videos(db)
    finally:
        db.close()

@scheduler.scheduled_job("interval", seconds=5)
def scheduled_job():
    scheduled_scrape()
    print("Scraping!")

scheduler.start()

@router.on_event("startup")
def startup_event():
    if not scheduler.running:
        scheduler.start()

@router.get("/start-scheduler")
def start_scheduler():
    if not scheduler.running:
        scheduler.start()
    return {"message": "Scheduler started and scraping job is running every 10 minutes."}

@router.get("/stop-scheduler")
def stop_scheduler():
    scheduler.shutdown()
    return {"message": "Scheduler stopped."}

