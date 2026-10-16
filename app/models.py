from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone


@dataclass
class Task:
    id: int
    title: str
    priority: str = "medium"
    done: bool = False
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds")
    )

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(**data)
