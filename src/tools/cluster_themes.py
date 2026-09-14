import json
import os
import re
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_groq import ChatGroq
import yaml

# Pydantic models for structured output from LLM
class ThemeRaw(BaseModel):
    name: str
    description: str
    review_ids: List[str]

class ClusterResultRaw(BaseModel):
    themes: List[ThemeRaw]

# Final enriched output models
class Theme(BaseModel):
    name: str
    description: str
    review_ids: List[str]
    review_count: int
    avg_rating: float
    top_quote: str

class ClusterResult(BaseModel):
    themes: List[Theme]

def load_config() -> Dict[str, Any]:
    config_path = os.path.join(os.path.dirname(__file__), "..", "..", "config", "settings.yaml")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    return {}

def truncate_text(text: str, max_words: int = 50) -> str:
    words = text.split()
    if len(words) > max_words:
        return " ".join(words[:max_words]) + "..."
    return text

def merge_smallest_themes(themes: List[ThemeRaw], max_themes: int) -> List[ThemeRaw]:
    """Merge the smallest themes locally until we hit max_themes."""
    if len(themes) <= max_themes:
        return themes
        
    # Sort themes by number of reviews, ascending
    sorted_themes = sorted(themes, key=lambda t: len(t.review_ids))
    
    while len(sorted_themes) > max_themes:
        # Take the two smallest themes and merge them
        t1 = sorted_themes.pop(0)
        t2 = sorted_themes.pop(0)
        
        merged_name = f"{t1.name} & {t2.name}"
        if len(merged_name) > 40:
            merged_name = "Miscellaneous"
            
        merged_desc = f"Combined themes: {t1.description} and {t2.description}"
        merged_ids = list(set(t1.review_ids + t2.review_ids))
        
        merged_theme = ThemeRaw(
            name=merged_name,
            description=merged_desc[:100] + ("..." if len(merged_desc) > 100 else ""),
            review_ids=merged_ids
        )
        sorted_themes.append(merged_theme)
        # Re-sort to always merge smallest
        sorted_themes = sorted(sorted_themes, key=lambda t: len(t.review_ids))
        
    return sorted_themes

@tool
def cluster_themes(status_message: str) -> str:
    """
    Cluster app reviews into themes using Groq.
    Reads from data/reviews.json and saves output to data/themes.json.
    
    Args:
        status_message: A message from the previous step indicating completion.
        
    Returns:
        A string message indicating success.
    """
    if not os.path.exists("data/reviews.json"):
        return "Error: data/reviews.json not found."
        
    with open("data/reviews.json", "r") as f:
        reviews = json.load(f)
        
    if not reviews:
        return "No reviews to cluster."
        
    config = load_config()
    max_themes = config.get("clustering", {}).get("max_themes", 5)
    model_name = config.get("groq", {}).get("model", "llama-3.1-70b-versatile") # Fallback to llama3.1
    temperature = config.get("groq", {}).get("temperature", 0.3)
    
    # 1. Token optimization: map reviews to stripped-down payload
    # Also keep a lookup dictionary for computing metrics later
    review_lookup = {}
    optimized_reviews = []
    
    for r in reviews:
        if "reviewId" not in r or "content" not in r:
            continue
            
        r_id = str(r["reviewId"])
        review_lookup[r_id] = r
        
        optimized_reviews.append({
            "id": r_id,
            "c": truncate_text(r.get("content", ""), 50)
        })
        
    # Serialize to compact JSON
    reviews_json = json.dumps(optimized_reviews, separators=(',', ':'))
    
    # Load prompt
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "clustering.txt")
    with open(prompt_path, "r") as f:
        prompt_template = f.read()
        
    prompt = prompt_template.format(
        max_themes=max_themes,
        reviews_json=reviews_json
    )
    
    # 2. Call LLM
    # Groq handles JSON mode well if we enforce it.
    llm = ChatGroq(
        model=model_name,
        temperature=temperature
    )
    
    response = llm.invoke(prompt)
    content = response.content
    
    # 3. Parse output safely
    try:
        # Extract JSON if the model added markdown fences
        json_match = re.search(r"```(?:json)?\s*(.*?)\s*```", content, re.DOTALL)
        if json_match:
            json_str = json_match.group(1).strip()
        else:
            # Maybe it just output raw JSON without markdown fences, try to extract first [ or {
            start_idx = content.find('{')
            if start_idx == -1:
                start_idx = content.find('[')
            end_idx = content.rfind('}')
            if end_idx == -1 or content.rfind(']') > end_idx:
                end_idx = content.rfind(']')
                
            if start_idx != -1 and end_idx != -1:
                json_str = content[start_idx:end_idx+1]
            else:
                json_str = content
                
        parsed_data = json.loads(json_str)
        raw_result = ClusterResultRaw.model_validate(parsed_data)
    except Exception as e:
        # Fallback if parsing completely fails
        print(f"Error parsing LLM output: {e}")
        print(f"RAW CONTENT WAS:\n{content}\n")
        raw_result = ClusterResultRaw(themes=[ThemeRaw(
            name="General Feedback", 
            description="All reviews", 
            review_ids=[r["id"] for r in optimized_reviews]
        )])

    # 4. Local Validation
    
    # A. Enforce max themes
    themes_raw = merge_smallest_themes(raw_result.themes, max_themes)
    
    # B. Assign orphan reviews to the largest theme
    assigned_ids = set()
    for t in themes_raw:
        assigned_ids.update(t.review_ids)
        
    all_ids = set(review_lookup.keys())
    orphan_ids = all_ids - assigned_ids
    
    if orphan_ids and themes_raw:
        largest_theme = max(themes_raw, key=lambda t: len(t.review_ids))
        largest_theme.review_ids.extend(list(orphan_ids))
    elif orphan_ids and not themes_raw:
        # No themes generated at all
        themes_raw.append(ThemeRaw(
            name="General Feedback",
            description="All reviews",
            review_ids=list(orphan_ids)
        ))
        
    # C. Compute metrics & construct final output
    final_themes = []
    for t in themes_raw:
        valid_ids = [rid for rid in t.review_ids if rid in review_lookup]
        
        if not valid_ids:
            continue
            
        total_score = 0
        top_quote = ""
        max_thumbs = -1
        
        for rid in valid_ids:
            r = review_lookup[rid]
            # Handle score safely
            try:
                total_score += float(r.get("score", 0))
            except (ValueError, TypeError):
                pass
                
            # Handle thumbsUpCount safely
            try:
                thumbs = int(r.get("thumbsUpCount", 0))
            except (ValueError, TypeError):
                thumbs = 0
                
            if thumbs > max_thumbs:
                max_thumbs = thumbs
                top_quote = r.get("content", "")
                
        avg_rating = round(total_score / len(valid_ids), 2)
        
        # If no thumbs up found, just take the first review's content as top quote
        if max_thumbs <= 0 and valid_ids:
            top_quote = review_lookup[valid_ids[0]].get("content", "")
            
        final_themes.append(Theme(
            name=t.name,
            description=t.description,
            review_ids=valid_ids,
            review_count=len(valid_ids),
            avg_rating=avg_rating,
            top_quote=top_quote
        ))
        
    result_dict = ClusterResult(themes=final_themes).model_dump()
    
    # Save themes to disk so the FastAPI backend can serve them
    os.makedirs("data", exist_ok=True)
    with open("data/themes.json", "w") as f:
        json.dump(result_dict, f, indent=2)
        
    return f"Successfully clustered into {len(final_themes)} themes and saved to data/themes.json."
