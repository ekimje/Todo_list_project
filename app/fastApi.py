from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

from fastapi import FastAPI

from app.logic import filter_items_by_date, sort_items
from app.storage import TodoStorage

app = FastAPI(title="Todo API")
storage = TodoStorage(Path("todo_data.json"))
current_date = date.today()

@app.get("/helth")
def health() -> dict[str,str]:
    return {"staus":"ok"}

@app.get("/current-day")
def get_current_day() -> dict[str,str]:
    return {"current_date":current_date.isoformat()}

@app.get("/current-day/prev")
def move_prev_date() -> dict[str,str]:
    global current_date
    current_date-= timedelta(days=1)
    return {"current_date":current_date.isoformat()}

@app.get("/current-day/next")
def move_next_date() -> dict[str,str]:
    global current_date
    current_date += timedelta(days=1)
    return {"current_date":current_date.isoformat()}

@app.get("/todos")
def todos_for_current_date() -> dict[str,object]:
    items = sort_items(storage.load())
    filtered = filter_items_by_date(items,current_date)
    return{
        "current_date":current_date.isoformat(),
        "count":len(filtered),
        "todos":[
            {
                "text":item.text,
                "done":item.done,
                "created_at":item.create_at.isoformat(),
            } for item in filtered
        ],
    }
