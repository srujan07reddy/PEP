from .mailbox import Mailbox
from ..models.message import A2AMessage

class RoutingEngine:
    """
    Intelligently routes messages between agents.
    """
    def __init__(self, mailbox: Mailbox):
        self.mailbox = mailbox

    def route_message(self, sender: str, receiver: str, topic: str, payload: dict):
        msg = A2AMessage(sender=sender, receiver=receiver, topic=topic, payload=payload)
        self.mailbox.send(msg)
