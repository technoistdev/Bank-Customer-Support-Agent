import logging
import json
from langchain_groq import ChatGroq
from src.schemas.response import AgentResponse
from config.settings import settings
from config.prompts import BILLING_SYSTEM_PROMPT

logger = logging.getLogger(__name__)

def run_billing(query: str) -> AgentResponse:
    """Handles billing support queries."""
    try:
        logger.info(f"Running billing agent for query: {query}")
        llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model=settings.MODEL_NAME,
            temperature=0
        )
        
        messages = [
            ("system", BILLING_SYSTEM_PROMPT),
            ("human", query)
        ]
        
        response = llm.invoke(messages)
        content = response.content
        
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        data = json.loads(content)
        result = AgentResponse(**data)
        logger.debug(f"Billing response: {result}")
        return result
    except Exception as e:
        logger.error(f"Error in run_billing: {str(e)}")
        return AgentResponse(answer="I'm having trouble processing your billing request.", confidence=0.0, used_tool=False)
