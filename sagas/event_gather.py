import asyncio


async def do_gather(*coroutines, allowed_exc):
    pending = list(map(asyncio.ensure_future, coroutines))
    try:
        await asyncio.gather(*pending)
    except allowed_exc:
        for t in pending:
            t.cancel()
