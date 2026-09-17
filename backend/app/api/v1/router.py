from fastapi import APIRouter
from app.api.v1.endpoints import chat, reasoning, simulator, knowledge, conversation

api_router = APIRouter()
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
api_router.include_router(conversation.router, prefix="/conversation", tags=["Conversation"])
api_router.include_router(reasoning.router, prefix="/reasoning", tags=["Reasoning"])
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["Knowledge"])
api_router.include_router(simulator.router, prefix="/simulator", tags=["What-If Ecology Simulator"])
