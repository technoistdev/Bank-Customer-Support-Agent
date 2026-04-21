from enum import Enum
from pydantic import BaseModel
from typing import Optional

class QueryType(str, Enum):
    TECHNICAL = "TECHNICAL"
    BILLING = "BILLING"
    GENERAL = "GENERAL"

class TriageResult(BaseModel):
    is_bank_related: bool
    query_type: Optional[QueryType] = None
    reason: str
