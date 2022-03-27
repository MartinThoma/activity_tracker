"""Activity monitor"""

# Core Library modules
import datetime
import time
from pathlib import Path
from typing import Optional

# Third party modules
import requests
import xprintidle  # pip install xprintidle


def main(
    storage_path: Optional[Path] = None,
    token: Optional[str] = None,
    home_assistant_url: Optional[str] = None,
    threshold_in_s: int = 30,
) -> None:
    if storage_path is None:
        today = datetime.datetime.now()
        storage_path = Path.home() / Path(f"activity_log/{today:%Y-%m-%d}.csv")
    if token is None:
        # Core Library modules
        import uuid

        token = str(uuid.uuid4())
    if home_assistant_url is not None and home_assistant_url.endswith("/"):
        home_assistant_url = home_assistant_url[:-1]
        # e.g. "http://192.168.178.76:8123"

    print(f"Token: {token}")
    print(f"Store activity log at: {storage_path}")

    while True:
        if was_active(threshold_in_s):
            if home_assistant_url:
                ping(home_assistant_url, token)
            last_activity = store_locally(storage_path)
            print(f"last_activity: {last_activity}")
        time.sleep(threshold_in_s)


def was_active(threshold_in_s: int) -> bool:
    last_activity_in_s = float(xprintidle.idle_time() / 1000)
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
    last_activity = int(xprintidle.idle_time())
    with open(path, "a") as fp:
        fp.write(f"{now:%Y-%m-%d %H:%M:%S},{last_activity}\n")
    return last_activity


if __name__ == "__main__":
    main()
