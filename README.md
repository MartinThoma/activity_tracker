# activity_tracker

Log when you were using your computer.

## Install

Currently this is not a package. You need to install the prerequesites:

```bash
pip install -r requirements.txt
```

and then run it within this folder.

## Usage

```python
$ python cli.py --help
Usage: cli.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  log-activity
  visualize
```

Start tracking:

```
$ python cli.py log-activity
Token: 383d723a-85bb-4a88-89db-5e74fefa6ba3
Store activity log at: /home/moose/activity_log/2021-11-04.csv
last_activity: 150
...
```

Visualize:

```
$ python cli.py visualize --help
Usage: cli.py visualize [OPTIONS]

Options:
  -i, --input FILE   [required]
  -o, --output FILE  [required]
  --help             Show this message and exit.
```

This produces a CSV file [like this](https://gist.github.com/MartinThoma/d8dbccb795016bc5c1090b8f48c1ed0d).
