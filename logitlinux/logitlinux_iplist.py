"""
Log it, Linux! core module
"""

from pathlib import Path
from logging_configuration import configure_logging
from typing import Iterator
from datetime import datetime
from dataclasses import dataclass

import logging
import socket
import subprocess
import re

configure_logging()
logger = logging.getLogger(__name__)


def convert_timestamp(timestamp_str: str) -> datetime:
    try:
        if "/" in timestamp_str:
            try:
                return datetime.strptime(timestamp_str, "%d/%m/%Y %H:%M:%S")
            except ValueError:
                return datetime.strptime(timestamp_str, "%d/%m/%y %H:%M:%S")
        elif len(timestamp_str) == 15:
            dt = datetime.strptime(timestamp_str, "%b %d %H:%M:%S")
            return dt.replace(year=datetime.now().year)
    except ValueError:
        pass
    return datetime.max


@dataclass
class LinuxEvent:
    timestamp: str
    command: str
    user: str
    ipList: list[str]
    port: str

    def __init__(self, timestamp, command, user):
        self.timestamp = timestamp
        self.command = command
        self.user = user
        self.ipList = []
        self.port = ""

    def toString(self) -> str:
        ipList_str = "["
        for ip in self.ipList:
            ipList_str = ipList_str + ip + ","
        ipList_str += "]"
        return f"timestamp: {self.timestamp} user: {self.user} command: {self.command} ipList: {ipList_str} port: {self.port}"

    def populateIpList(self, parsed_journal: list) -> None:
        event_time = convert_timestamp(self.timestamp)
        for session in parsed_journal:
            sess_start = convert_timestamp(session["session_start"])
            sess_end = convert_timestamp(session["session_end"])
            if sess_start is not None:
                if self.user == session["user"] and event_time > sess_start and sess_end == datetime.max:
                    self.ipList.append(session["ip"])
            elif (
                self.user == session["user"]
                and event_time > convert_timestamp(session["session_start"])
                and event_time < convert_timestamp(session["session_end"])
            ):
                self.ipList.append(session["ip"])


def get_hostname() -> str:
    try:
        with Path("/etc/hostname").open() as f:
            return f.readline().strip() or socket.gethostname()
    except (FileNotFoundError, OSError):
        return subprocess.run(["hostname"], capture_output=True, text=True, check=True).stdout.strip()


def stream_ausearch() -> Iterator[str]:
    with subprocess.Popen(
        [
            "/usr/sbin/ausearch",
            "--key",
            "auditcmd",
            "--checkpoint",
            "/etc/audit/logitlinux_checkpoint.txt",
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


def events_to_log(events: list) -> None:
    file_log = Path("/var/log/command")
    with file_log.open("a") as f:
        for event in events:
            f.write(f"{event.toString()}\n")


if __name__ == "__main__":
    hostname = get_hostname()
    logger.info("Script execution begin.", extra={"hostname": hostname})
    parsed_audit = parse_audit()
    parsed_journal = parse_journal()

    eventClass_list = []
    for audit_event in parsed_audit:
        tempInst = LinuxEvent(audit_event["timestamp"], audit_event["command"], audit_event["user"])
        tempInst.populateIpList(parsed_journal)
        eventClass_list.append(tempInst)

    events_to_log(eventClass_list)
    logger.info("Script execution ended.", extra={"hostname": hostname})
