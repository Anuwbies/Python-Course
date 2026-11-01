from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

def run_tests(folder):
    result = subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=folder, check=False)
    return result.returncode

if __name__ == "__main__":
    with TemporaryDirectory() as folder:
        path = Path(folder)
        (path / "calc.py").write_text("def double(value):\n    return value * 2\n", encoding="utf-8")
        (path / "test_calc.py").write_text("from calc import double\n\ndef test_normal():\n    assert double(3) == 6\n\ndef test_zero():\n    assert double(0) == 0\n", encoding="utf-8")
        code = run_tests(path)
        print(f"Pipeline exit: {code}")
        raise SystemExit(code)
