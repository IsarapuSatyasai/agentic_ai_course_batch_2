from pydantic import BaseModel, Field
from config import ToolResult

class DeadLetterRequest(BaseModel):
    queue_name: str = Field(..., description="Name of the queue")
    limit: int = Field(10, description="Maximum number of dead letters to retrieve")

def explore_dead_letters(request: DeadLetterRequest) -> ToolResult:
    """MCP-Style tool: Explore dead letter queue (simulate tool calling)"""
    mock_data = [
        {"id": f"dl-{i}", "error":"Timeout", "payload": "Order failed"}
        for i in range(min(request.limit, 5))
    ]
    
    return ToolResult(
        data={
            "queue": request.queue_name,
            "total": len(mock_data),
            "samples": mock_data
        }
    )