import asyncio

from sagas import SagaBuilder


saga_builder = SagaBuilder.create()

saga = saga_builder.build()
if __name__ == "__main__":
    asyncio.run(saga.run(exceptions=(Exception, OSError)))

