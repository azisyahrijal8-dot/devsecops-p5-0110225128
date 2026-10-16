from app.cli import run
from app.models import Task
from app.storage import JsonStorage


def test_storage_roundtrip(tmp_path):
    s = JsonStorage(str(tmp_path / "x.json"))
    assert s.load() == []
    s.save([Task(id=1, title="A")])
    assert s.load()[0].title == "A"


def test_cli_flow(tmp_path, capsys):
    f = str(tmp_path / "c.json")
    assert run(["--file", f, "add", "Tugas 1", "-p", "high"]) == 0
    assert run(["--file", f, "done", "1"]) == 0
    assert run(["--file", f, "stats"]) == 0
    assert "Selesai: 1" in capsys.readouterr().out


def test_cli_invalid_priority(tmp_path):
    assert run(["--file", str(tmp_path / "c.json"), "add", "X", "-p", "zzz"]) == 2
    