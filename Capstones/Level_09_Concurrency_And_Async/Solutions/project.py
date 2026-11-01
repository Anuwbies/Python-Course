import asyncio
from pathlib import Path
from tempfile import TemporaryDirectory

async def count_files(paths, workers=2):
    paths = [Path(path) for path in paths]
    if type(workers) is not int or workers <= 0:
        raise ValueError("Invalid worker count")
    if len({path.name for path in paths}) != len(paths):
        raise ValueError("File names must be unique")
    queue = asyncio.Queue(maxsize=workers * 2)
    results = {}
    async def worker():
        while True:
            path = await queue.get()
            try:
                if path is None:
                    return
                try:
                    text = await asyncio.to_thread(path.read_text, encoding="utf-8")
                except (OSError, UnicodeError) as error:
                    results[path.name] = {"error": type(error).__name__}
                else:
                    results[path.name] = {"count": len(text.split())}
            finally:
                queue.task_done()
    async with asyncio.TaskGroup() as group:
        for _ in range(workers):
            group.create_task(worker())
        for path in paths:
            await queue.put(path)
        for _ in range(workers):
            await queue.put(None)
        await queue.join()
    return results

async def main():
    with TemporaryDirectory() as folder:
        base = Path(folder)
        (base / "a.txt").write_text("one two", encoding="utf-8")
        (base / "b.txt").write_text("three", encoding="utf-8")
        results = await count_files([base / "a.txt", base / "b.txt", base / "missing.txt"])
        for name in sorted(results):
            result = results[name]
            value = result["count"] if "count" in result else "ERROR " + result["error"]
            print(f"{name}: {value}")

if __name__ == "__main__":
    asyncio.run(main())
