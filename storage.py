from pathlib import Path
import json
import datetime

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
            return [
                TodoItem(
                    text=item["text"],
                    done=item["done"],
                    date=datetime.fromisoformat(item["date"])
                    )
                for item in raw_data
                ]
        
        except (json.JSONDecodeError, TypeError, ValueError):
            return []
    
    def save(self, items: list[TodoItem])->None:
        payload=[]
        for item in items:
            d = asdict(item)
            d["date"] = item.date.isoformat()
            payload.append(d)
            
        self.file.write_text(
            json.dumps(payload,indent=2,ensure_ascii=False),
            encoding="utf-8"
        )