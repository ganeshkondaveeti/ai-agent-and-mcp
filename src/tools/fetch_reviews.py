import datetime
from typing import List, Dict, Any

from langchain_core.tools import tool
from google_play_scraper import reviews, Sort

from src.config import load_config

import time
import logging

logger = logging.getLogger(__name__)

def get_reviews_from_play_store(app_id: str, max_reviews: int, window_weeks: int) -> List[Dict[str, Any]]:
    # Fetch reviews with retry logic
    max_retries = 3
    base_delay = 2
    
    result = None
    for attempt in range(max_retries):
        try:
            result, continuation_token = reviews(
                app_id,
                lang='en', # default
                country='in', # Groww is primarily Indian
                sort=Sort.NEWEST,
                count=max_reviews
            )
            break
        except Exception as e:
            logger.warning(f"⚠️ Play Store fetch failed (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt == max_retries - 1:
                logger.error("❌ Max retries reached for fetching Play Store reviews.")
                raise e
            time.sleep(base_delay ** (attempt + 1))
            
    if not result:
        logger.info("ℹ️ No reviews returned from the Play Store.")
        return []
    
    # Filter by date
    cutoff_date = datetime.datetime.now() - datetime.timedelta(weeks=window_weeks)
    filtered_reviews = []
    
    for r in result:
        # result[i]['at'] is a datetime object
        if 'at' in r and r['at'] >= cutoff_date:
            # Convert datetime to ISO string for JSON serialization
            r['at'] = r['at'].isoformat()
            if r.get('repliedAt'):
                r['repliedAt'] = r['repliedAt'].isoformat()
            filtered_reviews.append(r)
            
    if not filtered_reviews:
        logger.info(f"ℹ️ Found {len(result)} total reviews, but none in the last {window_weeks} weeks.")
        
    return filtered_reviews

@tool
def fetch_reviews(app_id: str, weeks: int) -> str:
    """
    Fetch recent Google Play Store reviews for the given app ID.
    
    Args:
        app_id: The Google Play Store app ID (e.g., 'com.nextbillion.groww').
        weeks: The number of weeks of reviews to fetch (e.g., 12).
        
    Returns:
        A string message indicating success and where the file is saved.
    """
    logger.info(f"📥 Fetching reviews for {app_id} over the last {weeks} weeks...")
    config = load_config()
    max_reviews = config['app'].get('max_reviews', 500)
    
    fetched = get_reviews_from_play_store(app_id, max_reviews, weeks)
    logger.info(f"✅ Successfully fetched {len(fetched)} reviews.")
    
    import json
    import os
    os.makedirs("data", exist_ok=True)
    with open("data/raw_fetched.json", "w") as f:
        json.dump(fetched, f)
        
    return f"Successfully fetched {len(fetched)} reviews and saved to data/raw_fetched.json."
