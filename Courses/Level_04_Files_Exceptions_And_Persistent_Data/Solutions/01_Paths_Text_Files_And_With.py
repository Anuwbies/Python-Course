from pathlib import Path
from tempfile import TemporaryDirectory

def write_note(path, text):
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)

def read_note(path):
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()

if __name__ == "__main__":
    with TemporaryDirectory() as folder:
        path = Path(folder) / "note.txt"
        write_note(path, "Study café")
        print(read_note(path))
