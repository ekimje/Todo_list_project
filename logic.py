from __future__ import annotations

from collections import defaultdict
from datetime import date
from typing import Iterable

from models import TodoItem

def sort_item(items: Iterable[TodoItem]) -> list[TodoItem]:
    if items is None:
        return []
    return sorted(items, key=lambda item: item.created_at, reverse=True)

def filter_item_by_date(items:Iterable[TodoItem], target_date: date) -> dict[date,list[TodoItem]]:
    return [item for item in items if item.created_at.date() == target_date]


def group_by_date(items: Iterable[TodoItem]) -> dict[date, list[TodoItem]]:
    grouped: dict[date, list[TodoItem]] = defaultdict(list)
    for item in items:
        grouped[item.create_at.date()].append(item)
    return dict(grouped)
    