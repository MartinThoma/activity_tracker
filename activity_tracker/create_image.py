# Core Library modules
import csv
import datetime
from pathlib import Path
from typing import List

# Third party modules
from PIL import Image


def read_activity_file(activity_csv: Path) -> List[datetime.datetime]:
    times = []
    with open(activity_csv, "rt", newline="") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",", quotechar='"')
        next(csvreader, None)  # skip the headers
        times = [datetime.datetime.fromisoformat(row[0]) for row in csvreader]
    return times


def visualize_activity_matplotlib(
    activity_timestamps: List[datetime.datetime], filepath: Path
) -> None:
    time_range = max(activity_timestamps) - min(activity_timestamps)
    width = int(time_range / datetime.timedelta(minutes=1)) + 1
    height = 50
    img = Image.new(mode="RGB", size=(width, height), color=(255, 255, 255))
    pix = img.load()

    for timestamp in activity_timestamps:
        x = to_x(min(activity_timestamps), timestamp)
        for y in range(height):
            pix[x, y] = (0, 0, 0)
    img.save(filepath)


def to_x(min_time: datetime.datetime, current_time: datetime.datetime) -> int:
    return int((current_time - min_time) / datetime.timedelta(minutes=1))


def visualize_activity_plotly(
    activity_timestamps: List[datetime.datetime], filepath: Path
) -> None:
    """
    Visualize activity using Plotly.

    This code was written by AzuxirenLeadGuy:
    https://stackoverflow.com/a/69836149/562769
    """
    # Third party modules
    import plotly.graph_objects as go

    fig = go.Figure()

    datelist = activity_timestamps

    # Normalize all timestamps by subtracting the first.
    timestamplist = list(datelist)
    length = len(datelist)

    fig.add_trace(
        go.Scatter(x=timestamplist, y=[0] * length, mode="markers", marker_size=20)
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(
        showgrid=False,
        zeroline=True,
        zerolinecolor="black",
        zerolinewidth=3,
        showticklabels=False,
    )
    fig.update_layout(
        height=200, plot_bgcolor="white", title=f"Activity on {min(datelist):%d.%m.%Y}"
    )
    fig.write_image(str(filepath))
    fig.show()
