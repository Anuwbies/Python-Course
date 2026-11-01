import asyncio

async def run_bounded(values, limit):
    if type(limit) is not int or limit <= 0:
        raise ValueError("Invalid limit")
    semaphore = asyncio.Semaphore(limit)
    active = 0
    maximum = 0
    async def operation(value):
        nonlocal active, maximum
        async with semaphore:
            active += 1
            maximum = max(maximum, active)
            try:
                await asyncio.sleep(0)
                return value * 2
            finally:
                active -= 1
    results = await asyncio.gather(*(operation(value) for value in values))
    return results, maximum

async def main():
    results, maximum = await run_bounded([1, 2, 3], 2)
    print(results)
    print(f"Within limit: {maximum <= 2}")

if __name__ == "__main__":
    asyncio.run(main())
