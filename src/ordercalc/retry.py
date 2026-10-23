"""Simple retry with exponential backoff."""

import time
from collections.abc import Callable


def call_with_retry[T](
    fn: Callable[[], T],
    attempts: int = 3,
    backoff_s: float = 0.01,
    retry_on: tuple[type[Exception], ...] = (ConnectionError,),
) -> T:
    if attempts < 1:
        raise ValueError("attempts must be at least 1")
    attempt = 1
    while True:
        try:
            return fn()
        except retry_on:
            if attempt >= attempts:
                raise
            time.sleep(backoff_s * 2 ** (attempt - 1))
            attempt += 1
