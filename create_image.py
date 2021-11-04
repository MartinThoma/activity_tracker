from PIL import Image
from typing import List
from pathlib import Path
import datetime
import csv


def main(activity_csv: Path, image_filepath: Path):
    times = []
    with open(activity_csv, "rt", newline="") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",", quotechar='"')
        next(csvreader, None)  # skip the headers
        times = [datetime.datetime.fromisoformat(row[0]) for row in csvreader]

    visualize_activity(times, image_filepath)


def visualize_activity(activity_timestamps: List[datetime.datetime], filepath: Path):
    time_range = max(activity_timestamps) - min(activity_timestamps)
    width = int(time_range / datetime.timedelta(minutes=1)) + 1
    height = 50
    img = Image.new(mode="RGB", size=(width, height), color=(255, 255, 255))
    pix = img.load()

    for timestamp in activity_timestamps:
        x = to_x(min(activity_timestamps), timestamp)
        for y in range(height):
            pix[x, y] = (0, 0, 0)
    print(f"min: {min(activity_timestamps)}")
    print(f"max: {max(activity_timestamps)}")
    img.save(filepath)


def to_x(min_time: datetime.datetime, current_time: datetime.datetime) -> int:
    return int((current_time - min_time) / datetime.timedelta(minutes=1))
