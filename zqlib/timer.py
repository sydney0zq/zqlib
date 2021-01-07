from contextlib import contextmanager

__all__ = ['PTimer']

@contextmanager
def PTimer(description: str) -> None:
    """Simplest timer."""
    from time import time
    start = time()
    yield
    ellapsed_time = time() - start
    print(f"{description}: {ellapsed_time:.3f} seconds")


if __name__ == "__main__":
    import time
    with PTimer("unittest sleep"):
        time.sleep(2)
