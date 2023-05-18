from dataclasses import dataclass
from typing import Union
from uuid import UUID


@dataclass(frozen=True)
class AggregateId:
    id: Union[UUID, str]
