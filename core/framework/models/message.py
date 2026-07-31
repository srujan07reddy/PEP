from pydantic import BaseModel, Field
from typing import Any, Dict, Optional
from datetime import datetime
import uuid

class A2AMessage(BaseModel):
    id: str = Field(default_factory=lambda: f"msg-{uuid.uuid4().hex[:8]}")
    sender: str
    receiver: str
    topic: str
    payload: Dict[str, Any]
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
