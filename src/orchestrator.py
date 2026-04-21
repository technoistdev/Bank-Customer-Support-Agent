import logging
from src.agents.triage import run_triage
from src.agents.technical import run_technical
from src.agents.billing import run_billing
from src.agents.general import run_general
from src.tools.escalate import escalate
from src.schemas.query import QueryType

logger = logging.getLogger(__name__)

ESCALATION_THRESHOLD = 0.7

def handle(query: str) -> dict:
    """Main entry point to handle a customer query through the multi-agent system."""
    try:
        logger.info(f"Orchestrator received query: {query}")
        
        # 1. Triage
        triage_result = run_triage(query)
        
        if not triage_result.is_bank_related:
            logger.info("Query not bank-related. Redirecting.")
            return {
                "status": "redirect",
                "answer": "I'm sorry, I can only help with banking-related queries. How can I assist you with your bank account today?"
            }
        
        # 2. Routing
        agent_response = None
        agent_type = triage_result.query_type
        
        if agent_type == QueryType.TECHNICAL:
            agent_response = run_technical(query)
        elif agent_type == QueryType.BILLING:
            agent_response = run_billing(query)
        elif agent_type == QueryType.GENERAL:
            agent_response = run_general(query)
        else:
            logger.warning(f"Unknown agent type: {agent_type}. Defaulting to general.")
            agent_response = run_general(query)
            agent_type = QueryType.GENERAL

        # 3. Confidence Check & Escalation
        if agent_response.confidence >= ESCALATION_THRESHOLD:
            logger.info(f"Agent {agent_type} resolved query with confidence {agent_response.confidence}")
            return {
                "status": "resolved",
                "answer": agent_response.answer,
                "agent": agent_type,
                "used_tool": agent_response.used_tool
            }
        else:
            logger.info(f"Confidence {agent_response.confidence} below threshold {ESCALATION_THRESHOLD}. Escalating.")
            ticket = escalate.invoke({
                "original_query": query,
                "agent_type": str(agent_type),
                "agent_answer": agent_response.answer,
                "reason": f"Low confidence score: {agent_response.confidence}"
            })
            return {
                "status": "escalated",
                "ticket": ticket
            }
            
    except Exception as e:
        logger.error(f"Error in orchestrator: {str(e)}")
        return {
            "status": "error",
            "message": "An internal error occurred while processing your request."
        }
