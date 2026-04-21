import logging
import json
from langchain_groq import ChatGroq
from src.schemas.query import TriageResult
from src.tools.faq_lookup import faq_lookup
from config.settings import settings
from config.prompts import TRIAGE_SYSTEM_PROMPT

logger = logging.getLogger(__name__)

def run_triage(query: str) -> TriageResult:
    """Classifies the query and decides if it's bank-related and what type it is."""
    try:
        logger.info(f"Running triage for query: {query}")
        llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model=settings.MODEL_NAME,
            temperature=0
        ).bind_tools([faq_lookup])
        
        messages = [
            ("system", TRIAGE_SYSTEM_PROMPT),
            ("human", query)
        ]
        
        response = llm.invoke(messages)
        
        # Check if the LLM called the FAQ tool
        if response.tool_calls:
            for tool_call in response.tool_calls:
                if tool_call["name"] == "faq_lookup":
                    logger.info("Triage agent called faq_lookup")
                    faq_res = faq_lookup.invoke(tool_call["args"])
                    # Provide the FAQ result back to the model to refine its triage or just respond
                    messages.append(response)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "name": "faq_lookup",
                        "content": faq_res
                    })
                    response = llm.invoke(messages)

        # Parse the JSON response
        content = response.content
        if isinstance(content, list): # For some reason LangChain sometimes returns a list of blocks
            content = content[0].get("text", "")
        
        # Simple extraction if model wraps in code blocks
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        data = json.loads(content)
        result = TriageResult(**data)
        logger.debug(f"Triage result: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error in run_triage: {str(e)}")
        return TriageResult(is_bank_related=False, reason="Error during triage processing.")
