
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=5000,
        description="User's message to JOULE AI",
    )
    thread_id: str = Field(
        min_length=1,
        max_length=100,
        description="Conversation identifier",
    )


class ChatResponse(BaseModel):
    thread_id: str
    answer: str
    status: str = "success"
