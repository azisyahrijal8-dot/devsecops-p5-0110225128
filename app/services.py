from typing import List, Optional

from .models import Task
from .storage import JsonStorage
from .validators import validate_priority, validate_title


class TaskService:
    """Logika bisnis pengelolaan tugas."""

    def __init__(self, storage: JsonStorage):
        self.storage = storage

    def add(self, title: str, priority: str = "medium") -> Task:
        title = validate_title(title)
        priority = validate_priority(priority)
        tasks = self.storage.load()
        new_id = max((t.id for t in tasks), default=0) + 1
        task = Task(id=new_id, title=title, priority=priority)
        tasks.append(task)
        self.storage.save(tasks)
        return task

    def list(self, only_pending: bool = False) -> List[Task]:
        tasks = self.storage.load()
        if only_pending:
            tasks = [t for t in tasks if not t.done]
        order = {"high": 0, "medium": 1, "low": 2}
        return sorted(tasks, key=lambda t: (order[t.priority], t.id))

    def complete(self, task_id: int) -> Optional[Task]:
        tasks = self.storage.load()
        for t in tasks:
            if t.id == task_id:
                t.done = True
                self.storage.save(tasks)
                return t
        return None

    def delete(self, task_id: int) -> bool:
        tasks = self.storage.load()
        remaining = [t for t in tasks if t.id != task_id]
        if len(remaining) == len(tasks):
            return False
        self.storage.save(remaining)
        return True

    def stats(self) -> dict:
        tasks = self.storage.load()
        done = sum(1 for t in tasks if t.done)
        return {"total": len(tasks), "done": done, "pending": len(tasks) - done}