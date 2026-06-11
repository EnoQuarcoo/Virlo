from apscheduler.schedulers.background import BackgroundScheduler
from app.services.campaign_agent import run_agent


scheduler = BackgroundScheduler()

job = scheduler.add_job(run_agent, 'interval', days=14)

scheduler.start()