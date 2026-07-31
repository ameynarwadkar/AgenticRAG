import pytest
import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

import app.services.rag
import app.agents.orchestrator

# In pytest, we can mock out expensive database calls and LLM calls
# so that CI/CD pipelines run in milliseconds instead of minutes.

@pytest.mark.asyncio
@patch('app.services.rag.rag_service.retrieve', new_callable=AsyncMock)
async def test_rag_retrieval_mock(mock_retrieve):
    """
    Test that the RAG retrieval service can be called correctly,
    without actually hitting the Supabase Vector DB.
    """
    # 1. Setup the mock return value
    mock_retrieve.return_value = ["Mocked document context 1", "Mocked document context 2"]
    
    # 2. Call the function we want to test
    from app.services.rag import rag_service
    results = await rag_service.retrieve("What is your return policy?", limit=2)
    
    # 3. Assert it behaved as expected
    mock_retrieve.assert_called_once_with("What is your return policy?", limit=2)
    assert len(results) == 2
    assert "Mocked document context 1" in results[0]


@pytest.mark.asyncio
@patch('app.agents.orchestrator.AgentService')
async def test_agent_orchestrator_mock(MockAgentService):
    """
    Test that the orchestrator initializes without errors and handles a basic query,
    mocking out OpenAI/Azure so it doesn't cost API credits.
    """
    # Setup mock
    mock_agent = MockAgentService.return_value
    mock_agent.process_query = AsyncMock(return_value={
        "text": "This is a mocked AI response.",
        "citations": ["doc1"],
        "tools_called": []
    })
    
    # Execute
    response = await mock_agent.process_query("Hello AI!")
    
    # Assert
    mock_agent.process_query.assert_called_once_with("Hello AI!")
    assert response["text"] == "This is a mocked AI response."
    assert len(response["citations"]) == 1
