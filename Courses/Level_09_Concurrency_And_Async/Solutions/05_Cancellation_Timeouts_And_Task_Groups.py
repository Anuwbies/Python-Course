import asyncio

async def work(events):
    try:
        await asyncio.sleep(1)
    finally:
        events.append("closed")

async def main():
    events = []
    try:
        async with asyncio.timeout(0):
            await work(events)
    except TimeoutError:
        print("Timed out")
    print(f"Cleaned up: {events == ['closed']}")

if __name__ == "__main__":
    asyncio.run(main())
