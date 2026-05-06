from __future__ import annotations

from collections import defaultdict
from datetime import date
from typing import Iterable

from app.models import TodoItem

def sort_items(items: Iterable[TodoItem] | None) -> list[TodoItem]:
    if items is None:
        return []
    return sorted(items, key=lambda item: item.created_at, reverse=True)

def filter_items_by_date(items:Iterable[TodoItem], target_date: date) -> list[TodoItem]:
    return [item for item in items if item.created_at.date() == target_date]


def group_by_date(items: Iterable[TodoItem]) -> dict[date, list[TodoItem]]:
    grouped: dict[date, list[TodoItem]] = defaultdict(list)
    for item in items:
        grouped[item.created_at.date()].append(item)
    return dict(grouped)
    
sort_item = sort_items
filter_item_by_date = filter_items_by_date