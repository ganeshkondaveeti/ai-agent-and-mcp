import os
import json
from typing import Dict, Any, List
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from .cluster_themes import load_config

def format_pulse(pulse_markdown: str, max_words: int) -> str:
    """Ensure the pulse markdown is within the word limit."""
    words = pulse_markdown.split()
    if len(words) <= max_words:
        return pulse_markdown
        
    # Naive truncation if LLM ignores limits
    truncated = " ".join(words[:max_words])
    return truncated + "\n\n*(Truncated to meet length limit)*"

@tool
def generate_pulse(status_message: str) -> str:
    """
    Generates a weekly markdown pulse note based on clustered themes.
    Reads from data/themes.json.
    Returns the generated markdown content.
    
    Args:
        status_message: A message from the previous step indicating completion.
    """
    if not os.path.exists("data/themes.json"):
        return "Error: data/themes.json not found."
        
    with open("data/themes.json", "r") as f:
        themes_result = json.load(f)
        
    themes = themes_result.get("themes", [])
    if not themes:
        return "# No insights this week\nThere were no valid themes to generate a pulse from."
        
    config = load_config()
    top_n = config.get("clustering", {}).get("top_themes_in_pulse", 3)
    max_words = config.get("pulse", {}).get("max_words", 250)
    num_quotes = config.get("pulse", {}).get("num_quotes", 3)
    num_action_ideas = config.get("pulse", {}).get("num_action_ideas", 3)
    
    model_name = config.get("groq", {}).get("model", "llama-3.1-70b-versatile")
    temperature = config.get("groq", {}).get("temperature", 0.3)
    
    # Sort themes by review_count descending to get top themes
    sorted_themes = sorted(themes, key=lambda t: t.get("review_count", 0), reverse=True)
    top_themes = sorted_themes[:top_n]
    
    # Token optimization: Send only the essential data to the LLM
    lean_themes = []
    for t in top_themes:
        lean_themes.append({
            "name": t.get("name"),
            "description": t.get("description"),
            "review_count": t.get("review_count"),
            "top_quote": t.get("top_quote", "")
        })
        
    themes_json = json.dumps(lean_themes, indent=2)
    
    # Load prompt
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "pulse_generation.txt")
    with open(prompt_path, "r") as f:
        prompt_template = f.read()
        
    prompt = prompt_template.format(
        top_n=top_n,
        num_quotes=num_quotes,
        num_actions=num_action_ideas,
        max_words=max_words,
        themes_json=themes_json
    )
    
    # Call LLM
    llm = ChatGroq(
        model=model_name,
        temperature=temperature
    )
    
    response = llm.invoke(prompt)
    content = str(response.content)
    
    # Strip markdown code fences if present (e.g. ```markdown ... ```)
    if content.startswith("```markdown"):
        content = content[11:]
        if content.endswith("```"):
            content = content[:-3]
    content = content.strip()
    
    final_pulse = format_pulse(content, max_words)
    
    # Save the pulse to disk for completeness
    with open("data/pulse.md", "w") as f:
        f.write(final_pulse)
        
    return final_pulse
