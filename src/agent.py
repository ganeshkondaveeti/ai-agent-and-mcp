from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage

from src.config import load_config
from src.tools.fetch_reviews import fetch_reviews
from src.tools.scrubber import scrub_pii
from src.tools.cluster_themes import cluster_themes
from src.tools.generate_pulse import generate_pulse
from src.tools.enrich_reviews import enrich_reviews
from src.db import aggregate_metrics

def create_pipeline_agent(mcp_tools: list):
    """
    Creates a LangGraph ReAct agent that wires all tools together.
    """
    config = load_config()
    model_name = config.get("groq", {}).get("model", "llama-3.1-70b-versatile")
    temperature = config.get("groq", {}).get("temperature", 0.3)
    
    # Initialize the Groq LLM for orchestration
    llm = ChatGroq(
        model=model_name,
        temperature=temperature
    )
    
    # Combine our local tools with the remote MCP tools
    tools = [
        fetch_reviews,
        scrub_pii,
        enrich_reviews,
        aggregate_metrics,
        cluster_themes,
        generate_pulse
    ] + mcp_tools
    
    system_prompt = """You are the Groww Weekly Pulse Agent. Your job is to execute the following pipeline in order:
1. Use `fetch_reviews` to fetch recent Google Play Store reviews for 'com.nextbillion.groww' (use 12 weeks).
2. Use `scrub_pii` to clean the fetched raw reviews. Pass the success message from step 1 into this tool.
3. Use `enrich_reviews` to locally categorize and score reviews into feature pods. Pass the success message from step 2 into this tool.
4. Use `aggregate_metrics` to upsert the enriched reviews into the SQLite historical database. Pass the success message from step 3 into this tool.
5. Use `cluster_themes` on the cleaned reviews to extract themes. Pass the success message from step 4 into this tool.
6. Use `generate_pulse` on the themes result to generate a Markdown pulse note. Pass the success message from step 5 into this tool.
7. Use `gmail_draft` to create an email draft containing the generated Markdown pulse. The subject should be "Groww Weekly Pulse".

Execute these steps sequentially. The tools have been optimized to read/write to the file system to save tokens. You only need to pass the status string returned by a tool into the next tool's argument. Do not skip any steps. Once you have drafted the email, inform the user that the pipeline is complete and provide the Draft details.
"""

    agent_executor = create_react_agent(llm, tools, prompt=SystemMessage(content=system_prompt))
    return agent_executor
