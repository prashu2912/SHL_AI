import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from agent import decide_intent, search_catalog, load_catalog

# Initialize FastAPI app
app = FastAPI(
    title="SHL Conversational Assessment Recommender MVP",
    description="Deterministic rule-based MVP API for recommending SHL assessments.",
    version="1.0.0"
)

# --- Pydantic Schemas ---

class Message(BaseModel):
    role: str = Field(..., description="Role of the message sender ('user' or 'assistant')")
    content: str = Field(..., description="Content of the message")

class ChatRequest(BaseModel):
    messages: List[Message] = Field(..., description="Stateless conversation history")

class Recommendation(BaseModel):
    name: str = Field(..., description="Name of the assessment")
    url: str = Field(..., description="URL of the assessment in the catalog")
    test_type: str = Field(..., description="Type of the test (e.g., K, P, C, S)")

class ChatResponse(BaseModel):
    reply: str = Field(..., description="Natural language response from the agent")
    recommendations: List[Recommendation] = Field(
        default_factory=list, 
        description="List of recommended assessments (1 to 10 max, empty if context gathering)"
    )
    end_of_conversation: bool = Field(
        default=False, 
        description="True if the agent considers the task complete"
    )

# --- Endpoints ---

@app.get("/")
def read_root():
    """Root endpoint to verify the API is running (prevents 404 on base URL)."""
    return {"message": "SHL Conversational Assessment Recommender API is running. Visit /docs for the API schema."}

@app.get("/health")
def health_check():
    """Health check endpoint required by the evaluator."""
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    """
    Main conversational endpoint.
    Takes the stateless conversation history and returns the agent's next reply and optional recommendations.
    """
    if not req.messages:
        raise HTTPException(status_code=400, detail="Messages array cannot be empty.")

    # Only look at the latest user message for deterministic intent routing
    user_text = req.messages[-1].content
    intent = decide_intent(user_text)
    catalog = load_catalog()

    if intent == "clarify":
        return ChatResponse(
            reply="What role and seniority are you hiring for? Do you need to assess any specific skills?",
            recommendations=[],
            end_of_conversation=False
        )

    if intent == "recommend":
        results = search_catalog(user_text, catalog)
        return ChatResponse(
            reply="Here are the relevant SHL assessments based on your requirements:",
            recommendations=results,
            end_of_conversation=True
        )
        
    if intent == "refine":
        # Simulate refinement by grabbing a broader set of results including the new constraint
        results = search_catalog(user_text + " java python opq", catalog) 
        return ChatResponse(
            reply="I've updated the shortlist with your new constraints.",
            recommendations=results,
            end_of_conversation=True
        )

    if intent == "compare":
        return ChatResponse(
            reply="The OPQ provides behavioral and personality insights, whereas the GSA tests pure cognitive ability and problem solving.",
            recommendations=[],
            end_of_conversation=False
        )

    # Fallback
    return ChatResponse(
        reply="Can you clarify your requirement?",
        recommendations=[],
        end_of_conversation=False
    )

# Run server programmatically if executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
