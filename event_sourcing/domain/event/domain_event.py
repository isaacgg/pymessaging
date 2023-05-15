import os
from typing import Dict

from event_sourcing.domain.event.message import Message


class DomainEvent(Message):
    company = os.getenv(key="COMPANY")
    message_type = "domain_event"
    parameters: Dict = NotImplemented
