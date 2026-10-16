import pytest

from app.services import TaskService
from app.storage import JsonStorage


@pytest.fixture
def service(tmp_path):
    return TaskService(JsonStorage(str(tmp_path / "t.json")))


def test_add_increments_id(service):
    assert service.add("A").id == 1
    assert service.add("B").id == 2


def test_list_sorted_by_priority(service):
    service.add("low task", "low")
    service.add("high task", "high")
    assert [t.title for t in service.list()] == ["high task", "low task"]


def test_complete_and_stats(service):
    t = service.add("A")
    service.add("B")
    assert service.complete(t.id).done is True
    assert service.stats() == {"total": 2, "done": 1, "pending": 1}
    assert len(service.list(only_pending=True)) == 1


def test_complete_missing(service):
    assert service.complete(99) is None


def test_delete(service):
    t = service.add("A")
    assert service.delete(t.id) is True
    assert service.delete(t.id) is False