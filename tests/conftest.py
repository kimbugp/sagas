import asyncio


def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
