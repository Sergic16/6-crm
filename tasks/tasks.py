
from typing import TypedDict, Optional
from datetime import date

PRIORITES = {"low", "med", "high"}


class Task(TypedDict):
    id: int
    title: str
    priority: str
    status: str
    tags: Optional[list[str]]
    due: Optional[date]


def make_task(id_: int, title: str, due: Optional[date] = None, priority: str = "med", tags: Optional[list[str]] = None) -> Task:
    if priority not in PRIORITES:
        raise ValueError("Не верный приоритет. Можно только low | med | high")
    task: Task = {
        "id": id_,
        "title": title,
        "priority": priority,
        "tags": tags,
        "status": "new",
        "due": due
    }
    return task
