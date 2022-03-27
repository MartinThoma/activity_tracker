"""Functions that enable the user to automatically start the activity tracker"""

# Core Library modules
import subprocess
import sys
from typing import List


def does_screen_session_exist_cli(session_name: str, verbose: bool = False) -> None:
    if does_screen_session_exist(session_name):
        if verbose:
            print(f"Screen session '{session_name}' exists")
        sys.exit(0)
    else:
        if verbose:
            print(f"Screen session '{session_name}' does NOT exist")
        sys.exit(1)


def does_screen_session_exist(session_name: str) -> bool:
    session_names = get_active_screen_sessions()
    return session_name in session_names


def conditional_start_screen_session(session_name: str, command: str) -> None:
    if not does_screen_session_exist(session_name):
        start_screen_session(session_name, command)


def start_screen_session(session_name: str, command: str) -> None:

    subprocess.run(
        ["screen", "-S", session_name, "-U", "-d", "-m", *command.split(" ")]
    )


def get_active_screen_sessions() -> List[str]:
    result = subprocess.run(["screen", "-ls"], stdout=subprocess.PIPE)
    output = result.stdout.decode("utf-8")
    if "No Sockets found" in output:
        return []
    assert "There is a screen on" in output

    # get lines
    lines = []
    for line in output.splitlines():
        if line.startswith("\t"):
            lines.append(line)

    # get session names
    session_names = []
    for line in lines:
        line = line.strip()
        line = line.split("\t")[0]
        line = line.split(".")[1]
        session_names.append(line)
    return session_names
