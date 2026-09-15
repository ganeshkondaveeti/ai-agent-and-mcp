import json
import os
import logging
from typing import List, Dict, Any
from langchain_core.tools import tool

logger = logging.getLogger(__name__)

FEATURE_PODS = {
    "Mutual Funds & SIP": ["mutual fund", "sip", "portfolio", "nav", "lumpsum", "mandate", "autopay"],
    "Stocks & F&O": ["stock", "shares", "f&o", "options", "trading", "intraday", "margin", "delivery"],
    "UPI & Instant Payments": ["upi", "payment", "bank", "transfer", "scan", "pay", "failed"],
    "KYC & Bank Onboarding": ["kyc", "onboarding", "document", "pan", "aadhar", "verify", "account", "login"],
    "App Performance & Latency": ["crash", "slow", "lag", "bug", "stuck", "loading", "update", "ui", "face id", "fingerprint"]
}

def analyze_sentiment(score: int, text: str) -> str:
    """Basic rule-based sentiment based primarily on score."""
    if not score:
        return "neutral"
    if score >= 4:
        return "positive"
    elif score <= 2:
        return "negative"
    else:
        # Score 3 is tricky, we can check text length or just call it neutral
        return "neutral"

def map_to_feature_pod(text: str) -> str:
    """Maps review text to a specific feature pod based on keyword matching."""
    text_lower = text.lower()
    
    # Count matches for each pod
    pod_scores = {pod: 0 for pod in FEATURE_PODS.keys()}
    
    for pod, keywords in FEATURE_PODS.items():
        for keyword in keywords:
            if keyword in text_lower:
                pod_scores[pod] += 1
                
    # Find pod with max matches
    best_pod = max(pod_scores, key=pod_scores.get)
    if pod_scores[best_pod] > 0:
        return best_pod
    
    # Fallback
    return "General Experience"

@tool
def enrich_reviews(status_message: str) -> str:
    """
    Enriches scrubbed reviews with local sentiment and feature pod categorizations.
    Reads from data/reviews.json and saves to data/enriched_reviews.json.
    
    Args:
        status_message: A message from the previous step indicating completion.
    """
    if not os.path.exists("data/reviews.json"):
        return "Error: data/reviews.json not found."
        
    with open("data/reviews.json", "r") as f:
        reviews = json.load(f)
        
    enriched = []
    for r in reviews:
        content = r.get("content", "")
        score = r.get("score")
        
        # Enrich
        sentiment = analyze_sentiment(score, content)
        pod = map_to_feature_pod(content)
        
        # Create enriched review
        enriched_r = r.copy()
        enriched_r["sentiment"] = sentiment
        enriched_r["feature_pod"] = pod
        enriched.append(enriched_r)
        
    with open("data/enriched_reviews.json", "w") as f:
        json.dump(enriched, f, indent=2)
        
    logger.info(f"✅ Enriched {len(enriched)} reviews with sentiment and feature pods.")
    return f"Successfully enriched {len(enriched)} reviews and saved to data/enriched_reviews.json."
