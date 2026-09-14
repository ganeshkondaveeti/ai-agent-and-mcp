import pytest
from unittest.mock import patch, MagicMock
from src.tools.cluster_themes import (
    truncate_text,
    merge_smallest_themes,
    cluster_themes,
    ThemeRaw
)

def test_truncate_text():
    text = "word " * 60
    truncated = truncate_text(text, max_words=50)
    words = truncated.split()
    assert len(words) == 50
    assert words[-1].endswith("...")
    
    short_text = "just a few words"
    assert truncate_text(short_text, max_words=50) == short_text

def test_merge_smallest_themes():
    themes = [
        ThemeRaw(name="T1", description="desc", review_ids=["1", "2"]),        # 2
        ThemeRaw(name="T2", description="desc", review_ids=["3", "4", "5"]),   # 3
        ThemeRaw(name="T3", description="desc", review_ids=["6"]),             # 1
        ThemeRaw(name="T4", description="desc", review_ids=["7", "8"]),        # 2
        ThemeRaw(name="T5", description="desc", review_ids=["9", "10", "11"]), # 3
        ThemeRaw(name="T6", description="desc", review_ids=["12"]),            # 1
    ]
    
    # Needs to merge from 6 to 5
    merged = merge_smallest_themes(themes, max_themes=5)
    assert len(merged) == 5
    
    # The smallest themes were T3(1) and T6(1). They should be merged.
    merged_theme = next(t for t in merged if "T3" in t.name or "T6" in t.name or t.name == "Miscellaneous")
    assert len(merged_theme.review_ids) == 2
    assert set(["6", "12"]).issubset(set(merged_theme.review_ids))

@patch("src.tools.cluster_themes.ChatGroq")
def test_cluster_themes_mocked(mock_chat_groq):
    # Mock LLM response
    mock_llm = MagicMock()
    mock_response = MagicMock()
    mock_response.content = '''
    {
      "themes": [
        {
          "name": "Support",
          "description": "Customer support issues",
          "review_ids": ["r1", "r2"]
        },
        {
          "name": "Praise",
          "description": "Good app",
          "review_ids": ["r3"]
        }
      ]
    }
    '''
    mock_llm.invoke.return_value = mock_response
    mock_chat_groq.return_value = mock_llm
    
    # Input reviews
    reviews = [
        {"reviewId": "r1", "content": "bad support", "score": "1", "thumbsUpCount": "5"},
        {"reviewId": "r2", "content": "no reply", "score": "1", "thumbsUpCount": "0"},
        {"reviewId": "r3", "content": "nice app", "score": "5", "thumbsUpCount": "10"},
        {"reviewId": "r4", "content": "this will be an orphan", "score": "3", "thumbsUpCount": "1"} # Orphan!
    ]
    
    # Call tool
    result = cluster_themes.invoke({"reviews": reviews})
    
    themes = result.get("themes", [])
    assert len(themes) == 2
    
    support_theme = next(t for t in themes if t["name"] == "Support")
    praise_theme = next(t for t in themes if t["name"] == "Praise")
    
    assert support_theme["review_count"] == 3
    # Top quote should be 'bad support' because it has thumbsUpCount=5 (r4 only has 1, r2 has 0)
    assert support_theme["top_quote"] == "bad support"
    
    # Orphan review "r4" should be assigned to the largest theme (Support)
    assert len(support_theme["review_ids"]) == 3
    assert "r4" in support_theme["review_ids"]
    assert praise_theme["review_count"] == 1

def test_cluster_themes_empty():
    result = cluster_themes.invoke({"reviews": []})
    assert result == {"themes": []}
