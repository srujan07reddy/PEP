from pathlib import Path
from typing import List
from .contracts import BaseService

class CommunicationService(BaseService):
    """
    Provides access to Agent-to-Agent (A2A) communications.
    """
    def query_messages(self) -> str:
        """Fetch the latest Agent-to-Agent (A2A) messages."""
        # Note: In a fully fleshed out system, this would interact directly
        # with the Mailbox or MessageBus abstraction instead of file parsing.
        # But since Mailbox itself just writes to this file, we read it.
        messages_file = Path(self.workspace_root) / "workspaces" / ".system" / "messages.jsonl"
        if not messages_file.exists():
            return "No A2A messages found."
        
        try:
            with open(messages_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if not lines:
                    return "No A2A messages found."
                # Return the last 5 messages for brevity
                return "[" + ",".join([line.strip() for line in lines[-5:]]) + "]"
        except Exception as e:
            return f"Error reading messages: {e}"
