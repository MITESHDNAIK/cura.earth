"""
Pytest Fixtures and Global Test Configuration
"""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.memory import session_memory


@pytest.fixture
def clean_memory():
    """
    Cleans up session memory before and after test execution.
    """
    session_memory._sessions.clear()
    yield
    session_memory._sessions.clear()


@pytest.fixture
async def async_client():
    """
    Async HTTP client for FastAPI integration testing.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
