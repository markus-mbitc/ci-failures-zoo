import pytest

from ordercalc.retry import call_with_retry


def test_returns_on_first_success() -> None:
    assert call_with_retry(lambda: 42) == 42


def test_retries_until_success() -> None:
    calls = {"n": 0}

    def flaky_backend() -> str:
        calls["n"] += 1
        if calls["n"] < 3:
            raise ConnectionError("backend not ready")
        return "ok"

    assert call_with_retry(flaky_backend, attempts=3, backoff_s=0) == "ok"
    assert calls["n"] == 3


def test_gives_up_after_max_attempts() -> None:
    def always_down() -> str:
        raise ConnectionError("backend down")

    with pytest.raises(ConnectionError):
        call_with_retry(always_down, attempts=3, backoff_s=0)
