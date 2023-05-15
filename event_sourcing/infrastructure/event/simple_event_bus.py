from typing import List

from event_sourcing.domain.event.event_bus import EventBus
from event_sourcing.domain.event.message import Message
from event_sourcing.domain.event.message_publisher import MessagePublisher


class SimpleEventBus(EventBus):
    def __init__(self, publishers: List[MessagePublisher]):
        self._publishers = publishers
        self._declare_channels()

    def _declare_channels(self):
        for publisher in self._publishers:
            publisher.declare_channel()

    def publish(self, events: List[Message]):
        for event in events:
            is_published = False
            for publisher in self._publishers:
                if publisher.is_publishable(event):
                    publisher.publish(event)
                    is_published = True

            if not is_published:
                ...  # TODO: Log here "event not published"
