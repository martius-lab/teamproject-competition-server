"""
Adds support for parallel processing for the server.
"""
import threading
from collections import deque

from typing import Callable, Generic, TypeVar
from twisted.internet import reactor


def extern(func):
    """Call a function with the given arguments and keyword arguments."""

    def _f(*args, **kwargs):
        reactor.callInThread(func, *args, **kwargs)

    return _f


def intern(func):
    """Call a function with the given arguments and keyword arguments."""

    def _f(*args, **kwargs):
        return reactor.callFromThread(func, *args, **kwargs)

    return _f


T = TypeVar("T")


class Consumer(Generic[T]):
    """
    A class that represents a consumer for processing items from a queue in parallel.

    Args:
        worker (Callable[[list[T]], None]): The worker function that processes a batch.
        batch_size (int, optional): The number of items to process in each batch.
        instances (int, optional): The number of worker instances to create.
    """

    def __init__(
        self, worker: Callable[[list[T]], None], batch_size: int = 1, instances: int = 1
    ):
        self.func = worker
        self.batch_size = batch_size
        self.queue: deque[T] = deque()
        self.running = True
        self.lock = threading.Lock()

        for _ in range(instances):
            self._worker()

    def add(self, item: T):
        """
        Adds an item to the queue for processing.

        Args:
            item (T): The item to be processed.
        """
        with self.lock:
            self.queue.append(item)

    @extern
    def _worker(self) -> None:
        """
        Internal worker function that processes items from the queue.
        """
        while True:
            batch: list[T] = []
            with self.lock:
                while len(batch) < self.batch_size and self.queue:
                    batch.append(self.queue.popleft())

            if not self.running and len(batch) == 0:
                break

            self.func(batch)

    def stop(self):
        """
        Stops the consumer from processing further items.
        """
        self.running = False
