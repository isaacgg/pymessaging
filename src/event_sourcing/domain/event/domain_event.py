import os

from event_sourcing.domain.event.message import Message


class DomainEvent(Message):
    def __init__(self, **kwargs):
        super(DomainEvent, self).__init__(company=os.getenv(key="COMPANY"),
                                          message_type="domain_event",
                                          **kwargs)
