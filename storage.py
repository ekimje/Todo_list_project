from pathlib import Path
import json

from dataclasses import asdict
from models import TodoItem

class Todostorage:
    def __init__(self,file:Path) -> None:
        self.file = file
        
    def load(self) -> list[TodoItem]:
        if not self.file.exists(): #파일 존재 x -> 빈 리스트 반환
            return []

        try:
            raw_data = json.loads(self.file.read_text(encoding="utf-8"))
            return [TodoItem(**item) for item in raw_data]
        
        except (json.JSONDecodeError, TypeError, ValueError):
            return []
        finally:
            self.root.destroy()
    
    def save(self, items: list[TodoItem])->None:
        print("start")
        payload=[asdict(item) for item in items]  
        self.file.write_text(json.dumps(payload,indent=2),encoding="utf-8",) 
        print("end")