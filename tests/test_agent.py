import pytest
from unittest.mock import patch, MagicMock
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from src.agent import create_pipeline_agent

@tool
def dummy_mcp_tool_1():
    """Dummy MCP tool 1"""
    return "ok"

@tool
def dummy_mcp_tool_2():
    """Dummy MCP tool 2"""
    return "ok"

def test_create_pipeline_agent():
    # Provide fake MCP tools
    mcp_tools = [dummy_mcp_tool_1, dummy_mcp_tool_2]
    
    # Create the agent
    agent = create_pipeline_agent(mcp_tools)
    
    # Verify it returns a CompiledGraph (which is what create_react_agent returns in langgraph)
    assert hasattr(agent, "astream")
    assert hasattr(agent, "invoke")
    
    # We can inspect the tools bound to the agent.
    # In a langgraph ReAct agent, the tools are usually passed to the LLM node.
    # We can check if the expected tools are in the tools list passed to the graph
    # Let's verify the tools list length and names
    # Wait, create_react_agent hides the tools in the graph. We can verify our custom prompt is present.
    
    # The prompt should be a SystemMessage in the agent state or passed to the LLM.
    # Since we can't easily introspect the internal graph without breaking encapsulation,
    # we'll mock the ChatGoogleGenerativeAI and create_react_agent to inspect the arguments.
    pass

@patch('src.agent.ChatGoogleGenerativeAI')
@patch('src.agent.create_react_agent')
def test_agent_tool_registration(mock_create_react_agent, mock_llm):
    # Setup mock
    mock_create_react_agent.return_value = "fake_agent"
    
    mcp_tools = [dummy_mcp_tool_1, dummy_mcp_tool_2]
    
    agent = create_pipeline_agent(mcp_tools)
    
    # Verify the LLM was created
    mock_llm.assert_called_once()
    
    # Verify create_react_agent was called with the LLM, combined tools, and the prompt
    mock_create_react_agent.assert_called_once()
    args, kwargs = mock_create_react_agent.call_args
    
    # Check the tools list passed to create_react_agent
    tools_passed = args[1]
    tool_names = [t.name for t in tools_passed]
    
    assert "fetch_reviews" in tool_names
    assert "scrub_pii" in tool_names
    assert "cluster_themes" in tool_names
    assert "generate_pulse" in tool_names
    assert "dummy_mcp_tool_1" in tool_names
    assert "dummy_mcp_tool_2" in tool_names
    assert len(tools_passed) == 6
    
    # Check the prompt
    assert "prompt" in kwargs
    prompt = kwargs["prompt"]
    assert isinstance(prompt, SystemMessage)
    assert "Groww Weekly Pulse Agent" in prompt.content
    assert "fetch_reviews" in prompt.content
    assert "scrub_pii" in prompt.content
    
    # Check the return value
    assert agent == "fake_agent"
