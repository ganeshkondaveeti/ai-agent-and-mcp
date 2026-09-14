import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import sys

from src.main import main as run_pipeline

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def scheduled_job():
    logger.info("⏰ Starting scheduled weekly pulse pipeline...")
    try:
        await run_pipeline()
        logger.info("✅ Scheduled pipeline completed successfully.")
    except Exception as e:
        logger.error(f"❌ Scheduled pipeline failed: {e}", exc_info=True)

async def main():
    logger.info("🔄 Initializing Groww Weekly Pulse Scheduler...")
    
    # Create the AsyncIOScheduler
    scheduler = AsyncIOScheduler()
    
    # Schedule the job to run every week (e.g., Monday at 9:00 AM)
    # You can customize this cron expression via environment variables if needed
    trigger = CronTrigger(
        day_of_week='mon',
        hour=9,
        minute=0
    )
    
    scheduler.add_job(
        scheduled_job,
        trigger=trigger,
        id='weekly_pulse_job',
        name='Groww Weekly Pulse Pipeline',
        replace_existing=True
    )
    
    logger.info("🗓️  Job scheduled! Waiting for the next execution time...")
    logger.info(f"Next run at: {trigger}")
    
    scheduler.start()
    
    # Keep the main thread alive for the scheduler
    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        logger.info("🛑 Shutting down scheduler...")
        scheduler.shutdown()
        sys.exit(0)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
