from datetime import datetime
import click
from create_image import main as visualize_main
from is_active import main as log_activity_main
from pathlib import Path


@click.group()
def entry_point():
    pass


@entry_point.command()
@click.option(
    "--path",
    default=Path.home() / Path(f"activity_log/{datetime.now():%Y-%m-%d}.csv"),
    type=click.Path(exists=False, dir_okay=False),
)
def log_activity(path: str):
    log_activity_main(Path(path))


@entry_point.command()
@click.option(
    "--input", "-i", type=click.Path(exists=True, dir_okay=False), required=True
)
@click.option(
    "--output", "-o", type=click.Path(exists=False, dir_okay=False), required=True
)
def visualize(input, output):
    visualize_main(input, output)


if __name__ == "__main__":
    entry_point()
