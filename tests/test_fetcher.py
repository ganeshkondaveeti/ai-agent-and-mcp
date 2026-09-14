import pytest
from unittest.mock import patch
import datetime

from src.tools.fetch_reviews import get_reviews_from_play_store

@patch('src.tools.fetch_reviews.reviews')
def test_get_reviews_from_play_store(mock_reviews):
    # Mock data
    now = datetime.datetime.now()
    mock_data = [
        {
            'reviewId': '1',
            'at': now - datetime.timedelta(weeks=1),
            'content': 'Great app!'
        },
        {
            'reviewId': '2',
            'at': now - datetime.timedelta(weeks=10),
            'content': 'Too old review'
        }
    ]
    mock_reviews.return_value = (mock_data, None)
    
    # 8 weeks window
    result = get_reviews_from_play_store('com.test.app', 100, 8)
    
    assert len(result) == 1
    assert result[0]['reviewId'] == '1'
    assert isinstance(result[0]['at'], str) # should be isoformat string
