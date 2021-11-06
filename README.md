[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![GitHub last commit](https://img.shields.io/github/last-commit/MartinThoma/activity_tracker)

# activity_tracker

Log when you were using your computer.

## Installation

This package is currently not on PyPI. You need to install it manually:

```bash
$ git clone git@github.com:MartinThoma/activity_tracker.git ~/activity_tracker
$ cd ~/activity_tracker
$ pip install -e .
```


## Usage

```bash
$ activity_tracker --help
Usage: activity_tracker [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  log-activity
  visualize
```

Start tracking:

```bash
$ activity_tracker log-activity
Token: 383d723a-85bb-4a88-89db-5e74fefa6ba3
Store activity log at: /home/moose/activity_log/2021-11-04.csv
last_activity: 150
...
```

This produces a CSV file [like this](https://gist.github.com/MartinThoma/d8dbccb795016bc5c1090b8f48c1ed0d). That CSV can be visualized via:

```bash
$ activity_tracker visualize --help
Usage: cli.py visualize [OPTIONS]

Options:
  -i, --input FILE   [required]
  -o, --output FILE  [required]
  --help             Show this message and exit.
```

## Start Tracking on Startup

This depends very much on your operating system.

### Ubuntu

You need to edit your crontab file:

```
sudo crontab -e -u your_user_name
```

At the bottom of the file, add this line:

```
@reboot python3 -m activity_tracker log-activity &
```

Please note that you need to install the Package as `python3 -m pip install -e .`
for this to work. You can have multiple different Python environments on your
system.
