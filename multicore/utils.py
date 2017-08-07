import math

from multicore import NUMBER_OF_WORKERS


def ranges(iterable, min_range_size=0, number_of_workers=None):
    """Return a set of ranges (start, end) points so an iterable can be passed
    in optimal chunks to a task."""

    count = len(iterable)
    delta = max(
        int(math.ceil(count * 1.0 / (number_of_workers or NUMBER_OF_WORKERS))),
        min_range_size
    )
    start = 0
    while start < count:
        end = min(start + delta, count)
        yield start, end
        start = end
