from collections import defaultdict

def sort_items(items):
    return sorted(items, key=lambda x:x.date, reverse=True)


def group_by_date(items):
    grouped = defaultdict(list)
    for item in items:
        grouped[item.date.date()].append(item)
    return grouped
    