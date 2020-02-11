import asyncio
import pytest


@pytest.fixture(scope='module')
def event_loop():
    """Fixture for the async event loop

    Yields:
        event loop
    """
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
