"""Activity monitor"""

import os
import time
import sys
from pathlib import Path
import datetime

import requests
import xprintidle  # pip install xprintidle


def was_active(threshold_in_s: int) -> bool:
    last_activity_in_s = xprintidle.idle_time() / 1000
    return last_activity_in_s < threshold_in_s


def ping(home_assistant: str, token: str) -> None:
    url = f"{home_assistant}/api/webhook/{token}"
    resp = requests.post(url)
    if resp.status_code != 200:
        print(f"Retrieved {resp.status_code} when pinging {url}")


def store_locally(path: Path) -> int:
    if not path.exists():
        with open(path, "w") as fp:
            fp.write("date,last_activity\n")
    now = datetime.datetime.now()
    last_activity = xprintidle.idle_time()
    with open(path, "a") as fp:
        fp.write(f"{now:%Y-%m-%d %H:%M:%S},{last_activity}\n")
    return last_activity


if __name__ == "__main__":
    if len(sys.argv) < 2:
        import uuid
        token = str(uuid.uuid4())
    else:
        token = sys.argv[1]

    threshold_in_s = 30
    home_assistant = "http://192.168.178.76:8123"  # no trailing slash please!
    
    print(f"Token: {token}")
    today = datetime.datetime.now()
    path = Path.home() / Path(f"activity_log/{today:%Y-%m-%d}.csv")
    print(f"Store activity log at: {path}")

    while True:
        if was_active(threshold_in_s):
            # ping(home_assistant, token)
            last_activity = store_locally(path)
            print(f"last_activity: {last_activity}")
        time.sleep(threshold_in_s)
