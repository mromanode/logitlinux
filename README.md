<h1 align="center">Log it, Linux!</h1>

<p align="center">
  <img src="images/logo.png" alt="penguin-logo" width="250px" height="250px"/>
  <br>
  <em>Log it, Linux! (LiL) is a small, 
      open-source auditing tool designed for Linux systems.
      It records every command executed across your system.
      Mainly optimized for Splunk.
  <br>
</p>

<p align="center">
  <a href="docs"><strong>Explore the docs »</strong></a>
  <br>
  <a href="docs\ausearch.md">View Demo</a>
  ·
  <a href="CONTRIBUTING.md">Contributing Guidelines</a>
  ·
  <a href="https://github.com/mromanode/logitlinux/issues/">Submit an Issue</a>
</p>

## About The Project

It directly address common security concerns, such as:
- How to log all commands executed in the system? 
  - Captures every command run across your entire system.
- How can we monitor and track all the commands being executed on the system? 
  - Provides a detailed log file of all command activity.
- How to log every command executed by a specific user?
  - You can filter the log file by user.

## Setup

### Prerequisites
- Python 3
- Audit
- Mainly tested on RHEL 7 and later.

### Installation

Clone the repo and execute `setup.py`
```
git clone https://github.com/mromanode/logitlinux.git && python3 setup.py
```

## Usage

The usage is basic. Start, stop, restart and monitor the script using systemd.
```
# systemctl start logitlinux.service
# systemctl stop logitlinux.service
# systemctl restart logitlinux.service
# systemctl status logitlinux.service
```

To view the logs, the events are writte in `/var/log/command`

You can cat, tail and grep, such as:
```
$ cat /var/log/command
$ tail [-f] /var/log/command
$ cat /var/log/command | grep "user"
```

## Contact

Marco Romano - mromanode@gmail.com
Alessandro Manenti