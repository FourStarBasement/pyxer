from dataclasses import dataclass
from datetime import datetime

@dataclass
class Timestamped:
    createdAt: datetime
    updatedAt: datetime
    deletedAt: datetime

@dataclass
class Resource:
    id: int
    type: str
    relid: int
    url: str
    store: str
    remotePath: str
    meta: str = None
