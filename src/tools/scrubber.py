import re
import json
import os
from typing import List, Dict, Any

from langchain_core.tools import tool
from langdetect import detect, LangDetectException

# Regex patterns
EMAIL_REGEX = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
PHONE_REGEX = re.compile(r'\b(?:\+91[\-\s]?)?[0-9]{10}\b')
AADHAR_REGEX = re.compile(r'\b\d{4}\s?\d{4}\s?\d{4}\b')
PAN_REGEX = re.compile(r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b')
DEVICE_ID_REGEX = re.compile(r'\b(?:imei|device\s*id)[\s:]*[0-9a-zA-Z]+\b', re.IGNORECASE)

def scrub_text(text: str) -> str:
    if not text:
        return ""
    text = EMAIL_REGEX.sub('[EMAIL]', text)
    text = PHONE_REGEX.sub('[PHONE]', text)
    text = AADHAR_REGEX.sub('[AADHAR]', text)
    text = PAN_REGEX.sub('[PAN]', text)
    text = DEVICE_ID_REGEX.sub('[DEVICE_ID]', text)
    return text

def is_valid_review(text: str) -> bool:
    if not text:
        return False
    words = text.split()
    if len(words) < 2:
        return False
    return True

import csv

def save_reviews(new_reviews: List[Dict[str, Any]], filepath: str = "data/reviews.json") -> None:
    """Save reviews to JSON and CSV with deduplication by reviewId."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    export_dir = os.path.join(os.path.dirname(filepath), "exports")
    os.makedirs(export_dir, exist_ok=True)
    csv_filepath = os.path.join(export_dir, "play_store.csv")
    
    existing_reviews = {}
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                for r in data:
                    if 'reviewId' in r:
                        existing_reviews[r['reviewId']] = r
        except json.JSONDecodeError:
            pass # File is empty or corrupted, start fresh
            
    # Merge new
    for r in new_reviews:
        if 'reviewId' in r:
            existing_reviews[r['reviewId']] = r
            
    # Write JSON back
    final_reviews = list(existing_reviews.values())
    with open(filepath, 'w') as f:
        json.dump(final_reviews, f, indent=2)
        
    # Write CSV
    if final_reviews:
        # Collect all possible keys for the header
        keys = set()
        for r in final_reviews:
            keys.update(r.keys())
        fieldnames = sorted(list(keys))
        
        with open(csv_filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in final_reviews:
                writer.writerow(r)

@tool
def scrub_pii(raw_reviews: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Scrub Personally Identifiable Information (PII) from a list of reviews.
    Removes fields like userName and userImage, and redacts emails and phone numbers in the text.
    Also saves the cleaned reviews to local storage (data/reviews.json).
    
    Args:
        raw_reviews: List of raw review dictionaries.
        
    Returns:
        List of cleaned review dictionaries.
    """
    clean_reviews = []
    
    for r in raw_reviews:
        content = r.get('content', '')
        if not isinstance(content, str) or not is_valid_review(content):
            continue
            
        # Create a copy to avoid mutating the original unnecessarily
        clean_r = r.copy()
        
        # Remove PII fields
        for field in ['userName', 'userImage', 'reviewerLanguage']:
            clean_r.pop(field, None)
            
        # Scrub text fields (google-play-scraper uses 'content')
        clean_r['content'] = scrub_text(content)
            
        clean_reviews.append(clean_r)
        
    # Save to data/reviews.json
    save_reviews(clean_reviews)
    
    return clean_reviews
