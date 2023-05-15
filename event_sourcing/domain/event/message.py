from abc import ABC, abstractmethod
from dataclasses import field, dataclass
from datetime import datetime
from typing import Dict
from uuid import UUID, uuid4


@dataclass(frozen=True)
class Message(ABC):
    message_id: UUID = field(default_factory=uuid4, init=False)
    occurred_on: datetime = field(default_factory=datetime.now, init=False)
    company: str = NotImplemented
    microservice: str = NotImplemented
    version: str = NotImplemented
    message_type: str = NotImplemented
    aggregate: str = NotImplemented
    action: str = NotImplemented
    parameters: Dict = NotImplemented

    def serialize(self) -> Dict:
        return {
            'data': {
                "id": str(self.message_id),
                "type": self.message_type,
                "occurred_on": self.occurred_on.isoformat(),
                "attributes": {
                    "id": self.aggregate,
                    "parameters": {k: v for k, v in self.parameters.items()},
                },
                'meta': {
                    "host": "host",
                    "some other info": "info"
                },
            },
        }

    routing_key = f"{company}.{microservice}.{version}.{message_type}.{aggregate}.{action}"
