import sqlite3
import json
import os
import logging
from typing import List, Dict, Any
import datetime

logger = logging.getLogger(__name__)

DB_PATH = "data/metrics.db"

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Time-series metrics by day and store
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_metrics (
            date TEXT,
            store TEXT,
            positive_count INTEGER DEFAULT 0,
            neutral_count INTEGER DEFAULT 0,
            negative_count INTEGER DEFAULT 0,
            total_score REAL DEFAULT 0,
            review_count INTEGER DEFAULT 0,
            PRIMARY KEY (date, store)
        )
    ''')
    
    # Feature pod aggregation by day
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feature_pod_metrics (
            date TEXT,
            pod_name TEXT,
            positive_count INTEGER DEFAULT 0,
            negative_count INTEGER DEFAULT 0,
            review_count INTEGER DEFAULT 0,
            PRIMARY KEY (date, pod_name)
        )
    ''')
    
    conn.commit()
    conn.close()

def aggregate_and_upsert_reviews():
    """Reads enriched_reviews.json and aggregates them into the SQLite database."""
    init_db()
    
    if not os.path.exists("data/enriched_reviews.json"):
        logger.error("No enriched reviews found to aggregate.")
        return
        
    with open("data/enriched_reviews.json", "r") as f:
        reviews = json.load(f)
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for r in reviews:
        # e.g., "2024-10-14T09:15:00Z" -> "2024-10-14"
        raw_date = r.get("at", datetime.datetime.now().isoformat())
        date_str = raw_date.split("T")[0]
        
        store = r.get("source", "android")
        sentiment = r.get("sentiment", "neutral")
        pod = r.get("feature_pod", "General Experience")
        score = r.get("score", 0)
        
        # 1. Update daily_metrics
        # Use UPSERT (INSERT ON CONFLICT)
        cursor.execute('''
            INSERT INTO daily_metrics (date, store, positive_count, neutral_count, negative_count, total_score, review_count)
            VALUES (?, ?, ?, ?, ?, ?, 1)
            ON CONFLICT(date, store) DO UPDATE SET
                positive_count = positive_count + excluded.positive_count,
                neutral_count = neutral_count + excluded.neutral_count,
                negative_count = negative_count + excluded.negative_count,
                total_score = total_score + excluded.total_score,
                review_count = review_count + 1
        ''', (
            date_str, 
            store, 
            1 if sentiment == 'positive' else 0,
            1 if sentiment == 'neutral' else 0,
            1 if sentiment == 'negative' else 0,
            score
        ))
        
        # 2. Update feature_pod_metrics
        cursor.execute('''
            INSERT INTO feature_pod_metrics (date, pod_name, positive_count, negative_count, review_count)
            VALUES (?, ?, ?, ?, 1)
            ON CONFLICT(date, pod_name) DO UPDATE SET
                positive_count = positive_count + excluded.positive_count,
                negative_count = negative_count + excluded.negative_count,
                review_count = review_count + 1
        ''', (
            date_str,
            pod,
            1 if sentiment == 'positive' else 0,
            1 if sentiment == 'negative' else 0
        ))
        
    conn.commit()
    conn.close()
    logger.info("✅ Successfully aggregated and upserted reviews into SQLite DB.")

from langchain_core.tools import tool

@tool
def aggregate_metrics(status_message: str) -> str:
    """
    Aggregates enriched reviews into the SQLite database.
    
    Args:
        status_message: A message from the previous step indicating completion.
    """
    try:
        aggregate_and_upsert_reviews()
        return "Successfully aggregated reviews into SQLite database."
    except Exception as e:
        logger.error(f"Failed to aggregate metrics: {e}")
        return f"Error: {e}"

if __name__ == "__main__":
    aggregate_and_upsert_reviews()
