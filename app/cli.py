import argparse

from .services import TaskService
from .storage import JsonStorage


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="tasktracker", description="Manajer tugas sederhana")
    p.add_argument("--file", default="tasks.json", help="Lokasi file penyimpanan")
    sub = p.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="Tambah tugas")
    add.add_argument("title")
    add.add_argument("-p", "--priority", default="medium")

    ls = sub.add_parser("list", help="Tampilkan tugas")
    ls.add_argument("--pending", action="store_true")

    done = sub.add_parser("done", help="Tandai tugas selesai")
    done.add_argument("id", type=int)

    rm = sub.add_parser("delete", help="Hapus tugas")
    rm.add_argument("id", type=int)

    sub.add_parser("stats", help="Statistik tugas")
    return p


def run(argv=None) -> int:
    args = build_parser().parse_args(argv)
    service = TaskService(JsonStorage(args.file))
    try:
        if args.command == "add":
            t = service.add(args.title, args.priority)
            print(f"Ditambahkan #{t.id}: {t.title} [{t.priority}]")
        elif args.command == "list":
            for t in service.list(args.pending):
                mark = "x" if t.done else " "
                print(f"[{mark}] #{t.id} {t.title} ({t.priority})")
        elif args.command == "done":
            t = service.complete(args.id)
            print("Selesai." if t else "Tugas tidak ditemukan.")
            return 0 if t else 1
        elif args.command == "delete":
            ok = service.delete(args.id)
            print("Dihapus." if ok else "Tugas tidak ditemukan.")
            return 0 if ok else 1
        elif args.command == "stats":
            s = service.stats()
            print(f"Total: {s['total']} | Selesai: {s['done']} | Pending: {s['pending']}")
    except ValueError as e:
        print(f"Error: {e}")
        return 2
    return 0