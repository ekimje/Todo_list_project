import datetime 
from dataclasses import dataclass,field


@dataclass
class TodoItem:
    text: str
    done: bool = False
    created_at : datetime = field(default_factory=datetime.now())