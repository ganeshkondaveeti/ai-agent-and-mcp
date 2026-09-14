import pytest
from unittest.mock import patch, MagicMock
from src.tools.generate_pulse import generate_pulse, format_pulse

def test_format_pulse():
    short_text = "This is a short text."
    assert format_pulse(short_text, max_words=10) == short_text
    
    long_text = "This text has exactly seven words in it"
    assert "Truncated to meet length limit" in format_pulse(long_text, max_words=5)
    
@patch("src.tools.generate_pulse.ChatGroq")
def test_generate_pulse_mocked(mock_chat_groq):
    mock_llm = MagicMock()
    mock_response = MagicMock()
    
    mock_markdown = """# Weekly Pulse
    
## Top Themes
1. Support
2. Crashes

## Quotes
> "App crashed"
> "No reply"

## Action Ideas
- Fix crashes
"""
    mock_response.content = mock_markdown
    mock_llm.invoke.return_value = mock_response
    mock_chat_groq.return_value = mock_llm
    
    sample_themes = {
        "themes": [
            {
                "name": "Support", 
                "description": "bad support", 
                "review_count": 10,
                "top_quote": "no reply"
            },
            {
                "name": "Crashes", 
                "description": "app crashes", 
                "review_count": 5,
                "top_quote": "App crashed"
            }
        ]
    }
    
    result = generate_pulse.invoke({"themes_result": sample_themes})
    
    assert "Weekly Pulse" in result
    assert "Top Themes" in result
    assert "Action Ideas" in result

def test_generate_pulse_empty():
    result = generate_pulse.invoke({"themes_result": {"themes": []}})
    assert "No insights this week" in result
