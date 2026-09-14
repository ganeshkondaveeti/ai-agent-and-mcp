import pytest
from unittest.mock import patch, AsyncMock
from src.main import run_agent_pipeline

@pytest.mark.asyncio
@patch('src.main.create_pipeline_agent')
async def test_integration_pipeline_fallback(mock_create_pipeline_agent, tmp_path, monkeypatch):
    """
    Integration test to verify the pipeline fallback mode correctly triggers
    and writes the output locally when MCP fails.
    """
    # Create a mock agent that yields fake events
    mock_agent = AsyncMock()
    
    async def fake_astream(*args, **kwargs):
        # Yield a fake AI response
        yield {"node": {"messages": [type('obj', (object,), {'type': 'ai', 'content': 'Starting...'})]}}
        # Yield a fake tool output for generate_pulse
        yield {"node": {"messages": [type('obj', (object,), {'type': 'tool', 'name': 'generate_pulse', 'content': '# Fake Pulse'})]}}
        
    mock_agent.astream = fake_astream
    mock_create_pipeline_agent.return_value = mock_agent
    
    # Run the pipeline in fallback mode
    # We monkeypatch the output directory to avoid writing to the real one during tests
    monkeypatch.chdir(tmp_path)
    import os
    os.makedirs("output", exist_ok=True)
    
    await run_agent_pipeline([], fallback=True)
    
    # Verify the local file was created
    output_files = os.listdir("output")
    assert len(output_files) == 1
    assert output_files[0].startswith("pulse_")
    assert output_files[0].endswith(".md")
    
    with open(f"output/{output_files[0]}", "r") as f:
        content = f.read()
        assert content == "# Fake Pulse"
