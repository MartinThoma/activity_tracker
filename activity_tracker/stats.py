# Core Library modules
import datetime
from types import ModuleType
from typing import Dict, List, Tuple

# Third party modules
import plotext as plt


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
        plot_activity(values)


def plot_activity(times: List[datetime.datetime], plt: ModuleType = plt) -> None:
    """
    Plot a daily activity graph.

    Credits to Savino Piccolomo for this:
    https://github.com/piccolomo/plotext/issues/83#issuecomment-1081700156
    """
    # plt.clf()
    # plt.clt()
    # to optionally clean the terminal
    plt.datetime.set_datetime_form(  # type: ignore
        date_form="", time_form="%H:%M"
    )  # Try also time_form="%H" for clearer x ticks !

    times_orig = times
    times = [plt.datetime.datetime_to_timestamp(el) for el in times]  # type: ignore

    plt.scatter(times, [1] * len(times), fillx=1, marker="hd", color="red")  # type: ignore
    d = times_orig[0]
    base = datetime.datetime(d.year, d.month, d.day)
    xticks = [base + datetime.timedelta(hours=i) for i in range(25)]
    xlabels = [plt.datetime.datetime_to_string(tick) for tick in xticks]  # type: ignore
    xticks = [plt.datetime.datetime_to_timestamp(tick) for tick in xticks]  # type: ignore
    plt.xticks(xticks, xlabels)  # type: ignore
    plt.yticks()  # type: ignore
    plt.xlim(xticks[0], xticks[-1])  # type: ignore
    plt.ylim(0, 1)  # type: ignore
    plt.frame(0)  # type: ignore
    plt.xaxis(1, "lower")  # type: ignore
    plt.xaxis(1, "upper")  # type: ignore
    plt.xlabel("Hours in The Day")  # type: ignore
    plt.title("Activity Tracker")  # type: ignore

    # Set the height you prefer or comment for maximum size
    plt.plotsize(None, 20)  # type: ignore

    plt.show()  # type: ignore


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
