![Tests](https://github.com/kimbugp/sagas/workflows/Tests/badge.svg) [![PyPI version](https://badge.fury.io/py/pysagas.svg)](https://badge.fury.io/py/pysagas) ![Publish](https://github.com/kimbugp/sagas/workflows/Publish/badge.svg)
# SAGAS

A simple async sagas implementation

## Installation

```
$ pip install pysagas
```
## Usage 

### Simple example

``` python
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


def decrement(amount, index):
    """Decrements array index by amount
    
    Args:
        amount (int): decrement value
        index (int): index of value to decrement        
    """    
    counter[index] -= amount
    return counter


saga_builder = SagaBuilder.create()

saga = saga_builder\
    .add_step(lambda: add(amount, 0), lambda: decrement(amount, 0))\
    .add_step(lambda: add(amount, 1), lambda: decrement(amount, 1))\
    .build()

if __name__ == "__main__":
    asyncio.run(saga.run(exceptions=(OSError)))
    print(counter)  # [40, 50]
```

### Failure example

If one step fails, the compensating functions for the executed steps run and the counter values are compensated

``` python
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
    raise Exception('error occurred')


def decrement(amount, index):
    """Decrements array index by amount

    Args:
        amount (int): decrement value
        index (int): index of value to decrement
    """
    counter[index] -= amount
    return counter


saga_builder = SagaBuilder.create()

saga = saga_builder\
    .add_step(lambda: add(amount, 0), lambda: decrement(amount, 0))\
    .add_step(lambda: add(amount, 1), lambda: decrement(amount, 1))\
    .build()

if __name__ == "__main__":
    asyncio.run(saga.run(exceptions=(OSError, Exception)))
    print(counter)  # [10, 20]
```
