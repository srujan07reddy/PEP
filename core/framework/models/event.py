from pydantic import BaseModel
from typing import Dict, Any

class Event(BaseModel):
    event_id: str
    event_type: str
    version: str
    
    source_service: str
    producer_domain: str
    
    trace_id: str
    timestamp: str
    
    payload: Dict[str, Any]
