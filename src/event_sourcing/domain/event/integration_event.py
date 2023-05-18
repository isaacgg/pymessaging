import os

from event_sourcing.domain.event.message import Message


class IntegrationEvent(Message):
    company = os.getenv(key="COMPANY")
    message_type = "integration_event"
    aggregate_id: str
