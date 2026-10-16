VALID_PRIORITIES = ("low", "medium", "high")
MAX_TITLE_LENGTH = 100


def validate_title(title: str) -> str:
    """Pastikan judul tidak kosong dan tidak terlalu panjang."""
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Judul tugas tidak boleh kosong")
    title = title.strip()
    if len(title) > MAX_TITLE_LENGTH:
        raise ValueError(f"Judul maksimal {MAX_TITLE_LENGTH} karakter")
    return title


def validate_priority(priority: str) -> str:
    """Pastikan prioritas salah satu dari low/medium/high."""
    priority = (priority or "").lower()
    if priority not in VALID_PRIORITIES:
        raise ValueError(f"Prioritas harus salah satu dari {VALID_PRIORITIES}")
    return priority