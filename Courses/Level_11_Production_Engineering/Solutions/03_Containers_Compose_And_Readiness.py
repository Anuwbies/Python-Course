from pathlib import Path
from shutil import copyfile
from tempfile import TemporaryDirectory

ASSETS = Path(__file__).resolve().parents[1] / "Assets"

def copy_assets(destination):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    names = ["Dockerfile", "compose.yaml", "requirements.txt", "service.py", ".dockerignore"]
    for name in names:
        copyfile(ASSETS / name, destination / name)
    return sorted(names)

if __name__ == "__main__":
    with TemporaryDirectory() as folder:
        print(copy_assets(folder))
