"""
Tests for API Routes & Contract Validation
"""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_health_check():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "api_version" in data


@pytest.mark.asyncio
async def test_chat_clarification_trigger():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Incomplete input (only vague query)
        payload = {"query": "Biodiversity is declining on my land"}
        response = await client.post("/api/v1/chat/chat", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["requires_clarification"] is True
        assert len(data["clarification_questions"]) > 0


@pytest.mark.asyncio
async def test_multi_metric_reasoning_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "soil": {"organic_carbon_pct": 0.3},
            "climate": {"rainfall_category": "low"},
            "land_use": {"crop_type": "monoculture wheat"},
            "spatial": {"region": "semi-arid"}
        }
        response = await client.post("/api/v1/reasoning/reason", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["requires_clarification"] is False
        assert len(data["interconnected_variables"]) >= 3
        assert len(data["recommendations"]) > 0
