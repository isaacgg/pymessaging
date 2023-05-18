import os

from event_sourcing.domain.event.message import Message


class DomainEvent(Message):
    company = os.getenv(key="COMPANY")
    message_type = "domain_event"
