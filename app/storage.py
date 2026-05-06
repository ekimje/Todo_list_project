from __future__ import annotations

from pathlib import Path
import json
from datetime import datetime
from dataclasses import asdict

from app.models import TodoItem

class Todostorage:
    def __init__(self,file_path:Path) -> None:
        self.file_path = file_path
        
    def load(self) -> list[TodoItem]:
        if not self.file_path.exists(): #파일 존재 x -> 빈 리스트 반환
            return []

        try:
            raw_data = json.loads(self.file_path.read_text(encoding="utf-8"))
            if not isinstance(raw_data,list):
                return []
            items: list[TodoItem] = []
            for item in raw_data:
                items.append(
                    TodoItem(
                        text=item["text"],
                        done=bool(item.get("done",False)),
                        created_at=datetime.fromisoformat(item["created_at"]),
                    )
                )
            return items
        except (json.JSONDecodeError, TypeError, ValueError,KeyError):
            return []
    
    def save(self, items: list[TodoItem])->None:
        payload:list[dict[str,object]]=[]
        for item in items:
            item_dict = asdict(item)
            item_dict["created_at"] = item.created_at.isoformat()
            payload.append(item_dict)

        self.file_path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )