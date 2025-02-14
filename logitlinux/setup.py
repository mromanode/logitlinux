"""
Log it, Linux! setup module
"""

from pathlib import Path
from logging_configuration import configure_logging

import logging
import socket
import subprocess

configure_logging()
logger = logging.getLogger(__name__)


def write_audit_rule(rule_file: str) -> None:
    hostname = socket.gethostname()
    try:
        logger.info("Writing audit rules to file: %s", rule_file, extra={"hostname": hostname})

        rule_file_path = Path(rule_file)
        with rule_file_path.open("a") as f:
            f.write("-a exit,always -F arch=b32 -S execve -k auditcmd")
            f.write("-a exit,always -F arch=b32 -S execve -k auditcmd")

        subprocess.run("augenrules --load")

        logger.info("Audit rules written successfully.", extra={"hostname": hostname})
    except (OSError, IOError, Exception) as err:
        logger.info("Writing audit rules failed with: %s", err, extra={"hostname": hostname})


def create_systemd_unit() -> None:
    hostname = socket.gethostname()
    try:
        rule_file_path = Path("/etc/systemd/system/logitlinux.service")

        logger.info("Writing systemd unit to: %s", rule_file_path, extra={"hostname": hostname})

        with rule_file_path.open("a") as f:
            f.write(
                """
[Unit]
Description=Log it, Linux! Service
After=network.target

[Service]
Type=idle
Restart=always
RestartSec=30
User=root
Group=root
ExecStart=/usr/bin/python3 /opt/logitlinux/logitlinux.py

[Install]
WantedBy=multi-user.target
                """
            )

        logger.info("Wrote systemd unit successfully.", extra={"hostname": hostname})
    except (OSError, IOError, Exception) as err:
        logger.info("Failed to write systemd unit with: %s", err, extra={"hostname": hostname})


def move_to_opt() -> None:
    hostname = socket.gethostname()
    try:
        opt_dict = Path("/opt/logitlinux")
        logger.info("Creating script directory to %s", opt_dict, extra={"hostname": hostname})
        opt_dict.mkdir(exist_ok=True)
        logger.info("Made script directory successfully.", extra={"hostname": hostname})
    except (OSError, IOError, Exception) as err:
        logger.info("Failed to create script directory: %s", err, extra={"hostname": hostname})

    try:
        logitlinux_script = Path("logitlinux.py")
        logging_configuration = Path("logging_configuration.py")
        logger.info(
            "Moving script to %s, %s",
            logitlinux_script,
            logging_configuration,
            extra={"hostname": hostname},
        )
        logitlinux_script.rename("/opt/logitlinux/logitlinux.py")
        logging_configuration.rename("/opt/logitlinux/logging_configuration.py")
        logger.info("Moved file successfully.", extra={"hostname": hostname})
    except (OSError, IOError, Exception) as err:
        logger.info("Failed to copy script directory: %s", err, extra={"hostname": hostname})


if __name__ == "__main__":
    write_audit_rule("/etc/audit/audit.rules")
    create_systemd_unit()
    move_to_opt()
