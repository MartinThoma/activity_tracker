# Core Library modules
import datetime
from typing import List, Tuple


def analyze(timestamps: List[datetime.datetime]) -> None:
    """
    Returns a tuple of timedelta objects representing the total time spent
    working and the total time spent resting.
    """
    time_ranges = get_continuous_times(timestamps, datetime.timedelta(minutes=5))
    total_time_range = max(timestamps) - min(timestamps)
    total_work_time = datetime.timedelta()
    for start, end in time_ranges:
        total_work_time += end - start
    print(
        f"Spend {total_work_time/datetime.timedelta(hours=1):0.1f} hours "
        f"in a {total_time_range/datetime.timedelta(hours=1):0.1f} time frame "
        f"in front of the computer."
    )
    print(f"Started at {min(timestamps)}, stopped at {max(timestamps)}.")
    print(f"Made {len(time_ranges) - 1} breaks.")


def get_continuous_times(
    timestamps: List[datetime.datetime],
    stickyness: datetime.timedelta,
) -> List[Tuple[datetime.datetime, datetime.datetime]]:
    """
    Returns a list of tuples of datetime objects representing the start and end
    times of each continuous period of activity.
    """
    assert len(timestamps) > 0
    start_time = None
    last_time = None
    time_ranges: List[Tuple[datetime.datetime, datetime.datetime]] = []
    for timestamp in timestamps:
        if start_time is None:
            start_time = timestamp
            continue
        assert start_time is not None
        if last_time is None:
            if timestamp - start_time < stickyness:
                last_time = timestamp
            else:
                time_ranges.append((start_time, start_time))
                start_time = timestamp
            continue
        assert last_time is not None
        if timestamp - last_time <= stickyness:
            last_time = timestamp
        else:
            if last_time is None:
                last_time = start_time
            time_ranges.append((start_time, last_time))
            start_time = timestamp
            last_time = timestamp
    if last_time is None:
        last_time = start_time
    assert start_time is not None
    assert last_time is not None
    time_ranges.append((start_time, last_time))
    return time_ranges
