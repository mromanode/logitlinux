"""
Log it, Linux! Logging configuration module
"""

import json
import logging
import logging.config


def configure_logging() -> None:
    CONFIG = """
{
    "version": 1,
    "disable_existing_loggers": false,
    "formatters": {
        "info_error": {
            "format": "%(asctime)s hostname=%(hostname)s logtype=%(levelname)s message=%(message)s",
            "datefmt": "%d/%m/%y %H:%M:%S"
        }
    },
    "handlers": {
        "info_file": {
            "class": "logging.FileHandler",
            "level": "INFO",
            "formatter": "info_error",
            "filename": "/var/log/command",
            "mode": "a"
        },
        "error_file": {
            "class": "logging.FileHandler",
            "level": "ERROR",
            "formatter": "info_error",
            "filename": "/var/log/command",
            "mode": "a"
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": [
            "info_file",
            "error_file"
        ]
    }
}
"""
    logging.config.dictConfig(json.loads(CONFIG))
