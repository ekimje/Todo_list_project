import datetime 
from dataclasses import dataclass,field


@dataclass
class TodoItem:
    text: str
    done: bool
    date : datetime = field(default_factory=datetime.now())