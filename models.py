from dataclasses import dataclass

@dataclass
class TodoItem:
    text : str
    done : bool