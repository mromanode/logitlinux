"""
Log it, Linux! core module
"""

from pathlib import Path
from logging_configuration import configure_logging
from collections.abc import Iterator
from datetime import datetime

import logging
import socket
import subprocess
import re

configure_logging()
logger = logging.getLogger(__name__)


def get_hostname() -> str:
    try:
        with Path("/etc/hostname").open() as f:
            return f.readline().strip()
    except (FileNotFoundError, OSError):
        return socket.gethostname()


def stream_ausearch() -> Iterator[str]:
    with subprocess.Popen(
        [
            "/usr/sbin/ausearch",
            "--key",
            "auditcmd",
            "--checkpoint",
            "/etc/audit/auditd_checkpoint.txt",
            "--start",
            "checkpoint",
            "--interpret",
        ],
        stdout=subprocess.PIPE,
        text=True,
    ) as proc:
        if proc.stdout is None:
            raise RuntimeError("ausearch produced no output")
        for line in proc.stdout:
            yield line.strip()


def parse_audit() -> list[dict[str, str]]:
    combined_regex = re.compile(
        r"(?:type=PROCTITLE.*msg=audit\((?P<timestamp>[^)]+)\.\d+:\d+\)\s.*proctitle=(?P<command>.*))"
        r"|(?:type=SYSCALL.*auid=(?P<user>\S+))"
    )
    events = []
    current_event = {}

    for line in stream_ausearch():
        if match := combined_regex.search(line):
            if match.group("timestamp"):
                current_event = {
                    "timestamp": match.group("timestamp"),
                    "command": match.group("command"),
                }
            elif user := match.group("user"):
                current_event["user"] = user
                if len(current_event) == 3:
                    events.append(current_event)
                    current_event = {}
    return events


def stream_journalctl() -> Iterator[str]:
    with subprocess.Popen(["journalctl", "/usr/sbin/sshd"], stdout=subprocess.PIPE, text=True) as proc:
        if proc.stdout is None:
            raise RuntimeError("journalctl produced no output")
        for line in proc.stdout:
            yield line.strip()


def parse_journal() -> list[dict[str, str]]:
    session_regex = re.compile(
        r"(?:(?P<session_start>[A-Z][a-z]{2}\s\d{2}\s\d{2}:\d{2}:\d{2}).*?sshd\[(?P<pid>\d+)\].*?"
        r"Accepted (?:password|key) for (?P<user>\w+).*?from (?P<ip>\d{1,3}(?:\.\d{1,3}){3}).*?port (?P<port>\d+))"
        r"|"
        r"(?P<session_end>[A-Z][a-z]{2}\s\d{2}\s\d{2}:\d{2}:\d{2}).*?sshd\[(?P<d_pid>\d+)\].*?"
        r"session closed for user (?P<d_user>\w+)"
    )

    active_sessions = {}
    events = []

    for line in stream_journalctl():
        if match := session_regex.search(line):
            groups = match.groupdict()
            if groups["session_start"]:
                pid = groups["pid"]
                active_sessions[pid] = {
                    "pid": pid,
                    "user": groups["user"],
                    "ip": groups["ip"],
                    "port": groups["port"],
                    "session_start": groups["session_start"],
                    "session_end": "Still logged in",
                }
            elif groups["session_end"]:
                pid = groups["d_pid"]
                if pid in active_sessions:
                    session = active_sessions[pid]
                    session["session_end"] = groups["session_end"]
                    events.append(session)
                    del active_sessions[pid]

    events.extend(active_sessions.values())
    return events


def convert_timestamp(timestamp_str: str) -> datetime:
    if "/" in timestamp_str:
        try:
            return datetime.strptime(timestamp_str, "%d/%m/%y %H:%M:%S")
        except ValueError:
            return datetime.max
    elif len(timestamp_str) == 15:
        try:
            dt = datetime.strptime(timestamp_str, "%b %d %H:%M:%S")
            return dt.replace(year=datetime.now().year)
        except ValueError:
            return datetime.max
    else:
        return datetime.max


def merge_events(audit_events: list[dict[str, str]], journal_events: list[dict[str, str]]) -> list[str]:
    hostname = get_hostname()
    formatted_events = []

    for audit_event in audit_events:
        audit_event["timestamp"] = convert_timestamp(audit_event["timestamp"])  # type: ignore

    for journal_event in journal_events:
        journal_event["session_start"] = convert_timestamp(journal_event["session_start"])  # type: ignore
        if journal_event["session_end"] == "Still logged in":
            journal_event["session_end"] = datetime.max  # type: ignore
        else:
            journal_event["session_end"] = convert_timestamp(journal_event["session_end"])  # type: ignore

    for audit_event in audit_events:
        for journal_event in journal_events:
            if (
                journal_event["user"] == audit_event["user"]
                and journal_event["session_start"] <= audit_event["timestamp"] <= journal_event["session_end"]
            ):
                if journal_event["session_end"] != datetime.max:
                    session_end_str = journal_event["session_end"].strftime("%Y-%m-%d %H:%M:%S")  # type: ignore
                else:
                    session_end_str = "Still logged in"

                session_start_str = journal_event["session_start"].strftime("%Y-%m-%d %H:%M:%S")  # type: ignore
                formatted_string = (
                    f"timestamp={audit_event['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} "  # type: ignore
                    f"hostname={hostname} "
                    f"user={journal_event['user']} "
                    f"session_start={session_start_str} "
                    f"session_end={session_end_str} "
                    f"logType=COMMAND command='{audit_event['command']}'"
                )
                formatted_events.append(formatted_string)
                break

    return formatted_events


if __name__ == "__main__":
    hostname = get_hostname()
    path_log = Path("/var/log/command")
    logger.info("Script execution begin.", extra={"hostname": hostname})

    parsed_audit = parse_audit()
    parsed_journal = parse_journal()
    merged_events_strings = merge_events(parsed_audit, parsed_journal)

    with path_log.open("a") as f:
        for line in merged_events_strings:
            f.write(f"{line}\n")

    logger.info("Script execution ended.", extra={"hostname": hostname})
