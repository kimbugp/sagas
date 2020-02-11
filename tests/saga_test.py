from sagas import Saga, SagaBuilder, Step


class BaseTestCase(object):
    def assertEqual(self, first, second, msg=None):
        """Fail if the two objects are unequal as determined by the '=='
           operator.
        """
        assert first == second, msg


class TestSaga(BaseTestCase):
    def test_run_step_succeeds(self, event_loop):
        counters = [0, 10]

        async def action():
            counters[0] += 1

        step_1 = Step(action)
        event_loop.run_until_complete(
            Saga([step_1]).run(exceptions=(OSError, Exception))
        )
        self.assertEqual(counters[0], 1)

    def test_multiple_steps_succeed(self, event_loop):
        counters = [0, 0, 0, 0]

        def action(index):
            counters[index] += 1

        step_0 = Step(lambda: action(0))
        step_1 = Step(lambda: action(1))
        step_2 = Step(lambda: action(2))
        step_3 = Step(lambda: action(3))

        event_loop.run_until_complete(
            Saga([step_0, step_1, step_2, step_3]).run(exceptions=(OSError))
        )
        self.assertEqual(counters, [1, 1, 1, 1])

    def test_step_fails(self, event_loop):
        counters = [0]

        async def action():
            counters[0] += 1
            raise Exception("test_step_fails")

        step_1 = Step(action)
        try:
            event_loop.run_until_complete(Saga([step_1]).run(exceptions=(OSError)))
        except Exception as error:
            assert isinstance(error, Exception) is True

    def test_compensation_succeeds(self, event_loop):
        counters = [0]

        async def action():
            counters[0] += 1
            raise Exception("test_step_fails")

        async def comp():
            counters[0] -= 1

        step_1 = Step(action, comp)
        event_loop.run_until_complete(
            Saga([step_1]).run(exceptions=(OSError, Exception))
        )
        self.assertEqual(counters[0], 0)


class TestSagaBuilder(BaseTestCase):
    def test_run_and_compensate(self, event_loop):
        counters = [0, 10]

        async def action():
            counters[0] += 1

        async def comp():
            counters[0] -= 1

        saga = SagaBuilder.create().add_step(action, comp).build()
        event_loop.run_until_complete(saga.run(exceptions=(OSError)))
        self.assertEqual(counters[0], 1)
