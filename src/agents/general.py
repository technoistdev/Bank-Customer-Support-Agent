import logging
import json
from langchain_groq import ChatGroq
from src.schemas.response import AgentResponse
from config.settings import settings
from config.prompts import GENERAL_SYSTEM_PROMPT

logger = logging.getLogger(__name__)

def run_general(query: str) -> AgentResponse:
    """Handles general support queries."""
    try:
        logger.info(f"Running general agent for query: {query}")
        llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model=settings.MODEL_NAME,
            temperature=0
        )
        
        messages = [
            ("system", GENERAL_SYSTEM_PROMPT),
            ("human", query)
        ]
        
        response = llm.invoke(messages)
        content = response.content
        
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        data = json.loads(content)
        result = AgentResponse(**data)
        logger.debug(f"General response: {result}")
        return result
    except Exception as e:
        logger.error(f"Error in run_general: {str(e)}")
        return AgentResponse(answer="I'm having trouble processing your request.", confidence=0.0, used_tool=False)
