import logging
import json
from langchain_groq import ChatGroq
from src.schemas.response import AgentResponse
from config.settings import settings
from config.prompts import TECHNICAL_SYSTEM_PROMPT

logger = logging.getLogger(__name__)

def run_technical(query: str) -> AgentResponse:
    """Handles technical support queries."""
    try:
        logger.info(f"Running technical agent for query: {query}")
        llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model=settings.MODEL_NAME,
            temperature=0
        )
        
        messages = [
            ("system", TECHNICAL_SYSTEM_PROMPT),
            ("human", query)
        ]
        
        response = llm.invoke(messages)
        content = response.content
        
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        data = json.loads(content)
        result = AgentResponse(**data)
        logger.debug(f"Technical response: {result}")
        return result
    except Exception as e:
        logger.error(f"Error in run_technical: {str(e)}")
        return AgentResponse(answer="I'm having trouble processing your technical request.", confidence=0.0, used_tool=False)
