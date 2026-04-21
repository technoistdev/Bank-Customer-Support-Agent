import json
import logging
from langchain.tools import tool

logger = logging.getLogger(__name__)

@tool
def faq_lookup(query: str) -> str:
    """Search for the best matching answer in the bank's FAQ list based on keyword overlap."""
    try:
        logger.info(f"Looking up FAQ for query: {query}")
        with open("data/faq.json", "r") as f:
            faqs = json.load(f)
        
        query_words = set(query.lower().split())
        best_match = None
        max_overlap = 0

        for faq in faqs:
            keywords = set(k.lower() for k in faq["keywords"])
            overlap = len(query_words.intersection(keywords))
            if overlap > max_overlap:
                max_overlap = overlap
                best_match = faq["answer"]
        
        if best_match:
            logger.debug(f"FAQ match found with overlap {max_overlap}")
            return best_match
        
        logger.info("No FAQ match found.")
        return "No FAQ match found."
    except Exception as e:
        logger.error(f"Error in faq_lookup: {str(e)}")
        return "Error searching FAQs."
