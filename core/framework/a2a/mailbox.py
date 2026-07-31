from typing import List, Optional
from ..models.message import A2AMessage

class Mailbox:
    """
    Centralized message bus for the A2A Layer.
    """
    def __init__(self):
        self.messages: List[A2AMessage] = []

    def send(self, message: A2AMessage):
        self.messages.append(message)
        print(f"      [Mailbox] Message routed: {message.sender} -> {message.receiver} (Topic: {message.topic})")
        
        # Persist for UI
        import os, json
        from pathlib import Path
        repo_root = Path(os.environ.get("WORKSPACE_ROOT", "d:/product-engineering-platform"))
        system_dir = repo_root / "workspaces" / ".system"
        system_dir.mkdir(parents=True, exist_ok=True)
        messages_file = system_dir / "messages.jsonl"
        try:
            with open(messages_file, "a", encoding="utf-8") as f:
                f.write(message.model_dump_json() + "\n")
        except Exception as e:
            print(f"[ERROR] Failed to persist A2A message: {e}")

    def fetch(self, receiver: str, unread_only: bool = True) -> List[A2AMessage]:
        # Simple fetch for now. Real implementation would mark as read.
        return [m for m in self.messages if m.receiver == receiver]
