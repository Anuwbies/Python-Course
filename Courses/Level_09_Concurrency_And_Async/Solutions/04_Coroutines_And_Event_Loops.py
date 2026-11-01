import asyncio

async def async_double(value):
    await asyncio.sleep(0)
    return value * 2

async def main():
    results = await asyncio.gather(*(async_double(value) for value in [1, 2, 3]))
    print(results)

if __name__ == "__main__":
    asyncio.run(main())
