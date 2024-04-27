from typing import TypeVar

T = TypeVar("T")


def zip_longest(*iters: list[T], default: T):
    lens = [len(x) for x in iters]
    for line in range(max(lens)):
        yield tuple(
            itr[line] if line < lens[i] else default
            for i, itr in enumerate(iters)
        )
