# TaskTracker — devsecops-p5-NIM

## 1. Nama Aplikasi & Fungsi
**TaskTracker** adalah aplikasi command-line untuk mengelola daftar tugas: menambah tugas
dengan prioritas (low/medium/high), melihat daftar (terurut prioritas), menandai selesai,
menghapus, dan menampilkan statistik. Data disimpan di file JSON.

## 2. Bahasa / Framework
- Python 3.12 (hanya standard library: `argparse`, `json`, `dataclasses`)
- Pytest untuk unit test
- Bandit untuk SAST

## 3. Cara Menjalankan
```bash
git clone https://github.com/<username>/devsecops-p5-NIM.git
cd devsecops-p5-NIM
pip install -r requirements.txt

python main.py add "Belajar CI/CD" -p high
python main.py add "Baca materi SAST"
python main.py list
python main.py done 1
python main.py stats

python -m pytest -v        # menjalankan unit test
```

## 4. Overview Pipeline CI/CD
Workflow: `.github/workflows/devsecops.yml`

| Item | Keterangan |
|------|-----------|
| Trigger | `push` ke `main` dan `pull_request` ke `main` |
| Runner | `ubuntu-latest` |
| Job `build` | Checkout, setup Python 3.12, install dependencies, jalankan `pytest` |
| Job `sast-scan` | `needs: build`; menjalankan **Bandit** pada `app/` dan `main.py`, lalu mengunggah laporan sebagai artifact |

```
push / PR ke main ──► build (install + unit test) ──► sast-scan (Bandit)
```

## Struktur Proyek
```
app/            models, validators, storage, services, cli
tests/          unit test
main.py         entry point
.github/workflows/devsecops.yml
```