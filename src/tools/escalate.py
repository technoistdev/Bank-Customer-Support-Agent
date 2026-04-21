import logging
from langchain.tools import tool
from src.schemas.response import EscalationTicket

logger = logging.getLogger(__name__)

@tool
def escalate(original_query: str, agent_type: str, agent_answer: str, reason: str) -> dict:
    """Escalates the customer query to a human agent and creates a support ticket."""
    try:
        logger.info(f"Escalating query: {original_query}")
        ticket = EscalationTicket(
            original_query=original_query,
            agent_type=agent_type,
            agent_answer=agent_answer,
            reason=reason
        )
        logger.debug(f"Escalation ticket created: {ticket.model_dump()}")
        return ticket.model_dump()
    except Exception as e:
        logger.error(f"Error in escalate tool: {str(e)}")
        return {"error": "Failed to create escalation ticket."}
