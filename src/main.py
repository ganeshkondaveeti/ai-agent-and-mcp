import asyncio
import os
import sys

from src.config import load_config
from src.mcp_integration import get_mcp_tools
from src.agent import create_pipeline_agent

import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    logger.info("🚀 Starting Groww Weekly Pulse AI Agent Pipeline...")
    
    # Load configuration
    config = load_config()
    
    # Check if output directory exists for fallback
    os.makedirs("output", exist_ok=True)
    
    # 1. Connect to MCP Server and get tools
    mcp_tools = []
    try:
        async with get_mcp_tools() as tools:
            mcp_tools = list(tools)
            await run_agent_pipeline(mcp_tools)
    except Exception as e:
        logger.error(f"⚠️ MCP Server is unreachable or failed: {e}")
        logger.info("🔄 Falling back to local agent pipeline (no MCP integration)...")
        await run_agent_pipeline(mcp_tools, fallback=True)

async def run_agent_pipeline(mcp_tools, fallback=False):
    # 2. Create the ReAct Agent with the available tools
    agent = create_pipeline_agent(mcp_tools)
    
    logger.info("🤖 Agent initialized. Starting pipeline execution...")
    
    # 3. Invoke the agent
    prompt = "Please run the full weekly pulse pipeline now."
    if fallback:
        prompt += " The MCP server is unavailable, so SKIP step 5 and step 6 (publishing to Docs and Email). Just generate the pulse, I will handle it manually."
    
    initial_state = {
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    last_tool_output = ""
    # Stream the events from the agent to show progress
    async for event in agent.astream(initial_state):
        for node, values in event.items():
            if "messages" in values:
                last_message = values["messages"][-1]
                if last_message.type == "ai" and last_message.content:
                    logger.info(f"🧠 AI: {last_message.content}")
                elif last_message.type == "tool":
                    output_snippet = last_message.content[:200]
                    logger.info(f"🛠️  Tool Output ({last_message.name}): {output_snippet}...")
                    if last_message.name == "generate_pulse":
                        last_tool_output = last_message.content
                    
    logger.info("✅ Pipeline complete!")
    
    if last_tool_output:
        # Save locally so the dashboard API can serve it
        now = datetime.datetime.now()
        week_num = now.isocalendar()[1]
        filename = f"output/pulse_{now.year}-W{week_num}.md"
        with open(filename, "w") as f:
            f.write(last_tool_output)
        logger.info(f"💾 Saved pulse locally to {filename}")

if __name__ == "__main__":
    # Suppress langchain deprecation warnings for cleaner output
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    
    # Run the main async function
    asyncio.run(main())
