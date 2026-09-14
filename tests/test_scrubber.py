import pytest
import os
import json
from src.tools.scrubber import scrub_pii, scrub_text

def test_scrub_text():
    assert scrub_text("Contact me at test@example.com") == "Contact me at [EMAIL]"
    assert scrub_text("Call 9876543210 please") == "Call [PHONE] please"
    assert scrub_text("My Aadhar is 1234 5678 9012") == "My Aadhar is [AADHAR]"
    assert scrub_text("PAN ABCDE1234F") == "PAN [PAN]"
    assert scrub_text("IMEI: 1234567890abcdef") == "[DEVICE_ID]"

def test_scrub_pii(tmp_path):
    # Setup mock reviews
    raw_reviews = [
        {
            'reviewId': '1',
            'userName': 'John Doe',
            'userImage': 'http://image.url',
            'reviewerLanguage': 'en',
            'content': 'Email me at john@doe.com for feedback. This app is really good and I love using it every day.'
        },
        {
            'reviewId': '2',
            'userName': 'Jane',
            'content': 'Great app. I have been using this application for many months and it works perfectly.'
        }
    ]
    
    # Patch save location for testing if we wanted to, but we can just let it save to data/reviews.json for now
    # or better, just test the clean output
    clean = scrub_pii.invoke({"raw_reviews": raw_reviews})
    
    assert len(clean) == 2
    assert 'userName' not in clean[0]
    assert 'userImage' not in clean[0]
    assert 'reviewerLanguage' not in clean[0]
    assert clean[0]['content'] == 'Email me at [EMAIL] for feedback. This app is really good and I love using it every day.'
    
    assert 'userName' not in clean[1]
    assert clean[1]['content'] == 'Great app. I have been using this application for many months and it works perfectly.'
