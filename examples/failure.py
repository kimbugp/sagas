import asyncio
from sagas import SagaBuilder

counter = [10, 20]
amount = 30


def add(amount, index):
    """Increments array index by amount

    Args:
        amount (int): increment value
        index (int): index of value to increment
    """
    counter[index] += amount
    raise Exception("error occurred")


def decrement(amount, index):
    """Decrements array index by amount

    Args:
        amount (int): decrement value
        index (int): index of value to decrement
    """
    counter[index] -= amount
    return counter


saga_builder = SagaBuilder.create()

saga = (
    saga_builder.add_step(lambda: add(amount, 0), lambda: decrement(amount, 0))
    .add_step(lambda: add(amount, 1), lambda: decrement(amount, 1))
    .build()
)

if __name__ == "__main__":
    asyncio.run(saga.run(exceptions=(OSError, Exception)))
    print(counter)  # [10, 20]
