from fastapi import FastAPI
from schemas import ChatRequest, ChatResponse
from langchain_core.messages import HumanMessage
from agents.joule_supervisor import app as joule_app

app=FastAPI(
    title="JOULE AI API",
    description="Enterprise AI copilot API",
    version="1.0.0",
)


from fastapi import FastAPI

app = FastAPI(
    title="JOULE AI API",
    description="Enterprise AI copilot API",
    version="1.0.0",
)


@app.get("/")
def home():
    return {
        "message": "Welcome to JOULE AI API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "JOULE AI",
    }



@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        response = joule_app.invoke(
            {
                "messages": [
                    HumanMessage(content=request.message)
                ]
            },
            config={
                "configurable": {
                    "thread_id": request.thread_id
                }
            }
        )

        answer = response["messages"][-1].content

        return ChatResponse(
            thread_id=request.thread_id,
            answer=answer,
            status="success",
        )

    except Exception:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=500,
            detail="JOULE AI could not process the request.",
        )
