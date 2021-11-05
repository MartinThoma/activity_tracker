# Core Library modules
from datetime import datetime
from pathlib import Path

# Third party modules
import click

# First party modules
from activity_tracker.create_image import main as visualize_main
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
def visualize(input: str, output: str) -> None:
    visualize_main(Path(input), Path(output))


if __name__ == "__main__":
    entry_point()
