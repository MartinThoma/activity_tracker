# Core Library modules
from datetime import datetime
from pathlib import Path

# Third party modules
import click

# First party modules
from activity_tracker.create_image import (
    read_activity_file,
    visualize_activity_matplotlib,
    visualize_activity_plotly,
)
from activity_tracker.is_active import main as log_activity_main


@click.group()
def entry_point() -> None:
    pass


@entry_point.command()
@click.option(
    "--path",
    default=Path.home() / Path(f"activity_log/{datetime.now():%Y-%m-%d}.csv"),
    type=click.Path(exists=False, dir_okay=False),
)
def log_activity(path: str) -> None:
    log_activity_main(Path(path))


@entry_point.command()
@click.option(
    "--input", "-i", type=click.Path(exists=True, dir_okay=False), required=True
)
@click.option(
    "--output", "-o", type=click.Path(exists=False, dir_okay=False), required=True
)
@click.option(
    "--renderer", type=click.Choice(["plotly", "matplotlib"]), default="plotly"
)
def visualize(input: str, output: str, renderer: str) -> None:
    activity = read_activity_file(Path(input))
    if renderer == "plotly":
        visualize_activity_plotly(activity, Path(output))
    elif renderer == "matplotlib":
        visualize_activity_matplotlib(activity, Path(output))
    else:
        print("Invalid choice")


if __name__ == "__main__":
    entry_point()
