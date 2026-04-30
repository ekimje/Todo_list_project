from pathlib import Path
from dataclasses import dataclass
import json

from .models import TodoItem

class Todostorage:
    def __init__(self,file:Path)->None:
        self.file = file
        
    def load(self)->list[TodoItem]:
        if not self.file.exists(): #파일 존재 x -> 빈 리스트 반환
            return []
    
    def save(self, items:list[TodoItem])->None:
        payload=[dataclass.asdict(item) for item in items]   
        