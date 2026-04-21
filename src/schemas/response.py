from pydantic import BaseModel

class AgentResponse(BaseModel):
    answer: str
    confidence: float
    used_tool: bool

class EscalationTicket(BaseModel):
    original_query: str
    agent_type: str
    agent_answer: str
    reason: str
