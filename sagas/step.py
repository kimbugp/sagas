import asyncio
from abc import abstractmethod
from inspect import iscoroutinefunction as is_coroutine
from .states import State, StepStates


class BaseStep(StepStates):
    async def do_run(self, *args, **kwargs):
        self._state = State.RUNNING
        try:
            res = await self.run(*args, **kwargs)
        except Exception as error:
            self._state = State.FAILURE
            raise error
        self._state = State.SUCCESS
        return res

    async def do_compensate(self, *args, **kwargs):
        self._state = State.RUNNING
        res = await self.compensate(*args, **kwargs)
        self._state = State.COMPENSATED
        return res

    @abstractmethod
    async def run(self, *args, **kwargs):
        pass

    @abstractmethod
    async def compensate(self, *args, **kwargs):
        pass


class Step(BaseStep):
    """
    Creates an saga step with a function to call with its compensation
    """

    def __init__(self, func, compensation=None):
        assert callable(func) is True, "'func' argument must be callable"
        self.func = func
        if compensation:
            assert callable(compensation) is True, "'func' argument must be callable"
            self.compensation = compensation

        super().__init__()

    async def _call_func(self, func, *args, executor=None, **kwargs):
        if is_coroutine(func):
            return await func(*args, **kwargs)
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(executor, func, *args, **kwargs)

    async def run(self, *args, **kwargs):
        return await self._call_func(self.func, *args, **kwargs)

    async def compensate(self, *args, **kwargs):
        return (
            await self._call_func(self.compensation, *args, **kwargs)
            if self.compensation
            else None
        )
