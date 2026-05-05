from __future__ import annotations

from collections import defaultdict
from datetime import date
from typing import Iterable

from models import TodoItem

def sort_items(items: Iterable[TodoItem]) -> list[TodoItem]:
    return sorted(items, key=lambda item:item.created_at, reverse=True)


def group_by_date(items:Iterable[TodoItem]) -> dict[date,list[TodoItem]]:
    grouped  : dict[items:Iterable[TodoItem]] = defaultdict(list)
    for item in items:
        grouped[item.create_at.date()].append(item)
    return dict(grouped)
    