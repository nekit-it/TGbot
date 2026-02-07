import asyncio

async def fake_progress(callback):
    for i in range(0, 101, 20):
        await asyncio.sleep(0.5)
        await callback(i)
