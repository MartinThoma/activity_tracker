# activity_tracker

Log when you were using your computer.

## Install

Currently this is not a package. You need to install the prerequesites:

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

This produces a CSV file [like this](https://gist.github.com/MartinThoma/d8dbccb795016bc5c1090b8f48c1ed0d).

You can visualize it via:

```bash
$ activity_tracker visualize --help
Usage: cli.py visualize [OPTIONS]

Options:
  -i, --input FILE   [required]
  -o, --output FILE  [required]
  --help             Show this message and exit.
```
