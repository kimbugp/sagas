import asyncio

from sagas import SagaBuilder

counter1 = 0
counter2 = 0

amount1 = 10
amount2 = 15


def count1():
    print('count 1')
    global counter1
    counter1 += amount1


def count2():
    print('count 2')
    global counter2
    counter2 += amount2
    raise Exception('some error happened')


def counter1():
    global counter1
    counter1 -= amount1
    print('compensating 1')


def counter2():
    global counter2
    counter2 -= amount2
    print('compensating 2')


def another():
    global counter2
    counter2 += amount2


saga_builder = SagaBuilder.create()

saga_builder.add_step(count2, counter2)
saga_builder.add_step(count1, counter1)

saga = saga_builder.build()
if __name__ == "__main__":
    asyncio.run(saga.run(exceptions=(Exception, OSError)))

