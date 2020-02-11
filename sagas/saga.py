from collections.abc import Sequence
from .event_gather import do_gather
from .states import State, StepStates
from .step import Step
from typing import List


class Saga(StepStates):
    steps: List[Step] = []

    def __init__(self, steps: list = None):
        if steps is None:
            steps = []
        assert isinstance(steps, Sequence), "Steps must be a sequence"
        self.steps = steps
        super().__init__()

    async def run(self, *args, executor=None, exceptions=None, **kwargs):
        futures = [step.do_run(*args, **kwargs) for step in self.steps]
        await do_gather(*futures, allowed_exc=(exceptions))
        failure = any([step.failure for step in self.steps])
        if failure:
            futures = [
                step.do_compensate(*args, **kwargs)
                for step in self.steps
                if step.processed
            ]
            await do_gather(*futures, allowed_exc=(exceptions))
        self._state = State.FAILURE if failure else State.SUCCESS


class SagaBuilder(object):
    def __init__(self):
        self.steps = []

    @staticmethod
    def create():
        return SagaBuilder()

    def add_step(self, func, compensation):
        step = Step(func, compensation)
        self.steps.append(step)
        return self

    def build(self):
        return Saga(self.steps)
