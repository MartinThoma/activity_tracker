# Core Library modules
import datetime
from typing import Dict, List, Tuple


def analyze(timestamps: List[datetime.datetime]) -> None:
    """
    Returns a tuple of timedelta objects representing the total time spent
    working and the total time spent resting.
    """
    analyze_contiguous(timestamps)
    grouped_by_day = group_by_day(timestamps)
    current_year = None
    current_month = None
    for date_str, values in sorted(grouped_by_day.items()):
        year, month, day = date_str.split("-")
        if year != current_year:
            current_year = year
            print(f"\n\n# {current_year}")
        if month != current_month:
            current_month = month
            print(f"\n\n## {current_month}")
        print(f"\n### {date_str}")
        analyze_contiguous(values)


def group_by_day(
    timestamps: List[datetime.datetime],
) -> Dict[str, List[datetime.datetime]]:
    """
    Returns a dictionary mapping each day of the week to a list of timestamps
    for that day.
    """
    grouped: Dict[str, List[datetime.datetime]] = {}
    for timestamp in timestamps:
        day = timestamp.strftime("%Y-%m-%d")
        if day not in grouped:
            grouped[day] = []
        grouped[day].append(timestamp)
    return grouped


def analyze_contiguous(timestamps: List[datetime.datetime]) -> None:
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
    for timestamp in sorted(timestamps):
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
