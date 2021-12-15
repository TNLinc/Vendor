import logging
import tempfile

from logstash_async.constants import constants

from core.config import settings


class DefaultFilter(logging.Filter):
    def __init__(self, param=None):
        super().__init__()
        self.param = param

    def filter(self, record):
        record.tags = settings.PROJECT_NAME
        return True


constants.ERROR_LOG_RATE_LIMIT = "2 per hour"

_grey = "\x1b[38;21m"
_blue = "\u001b[34;1m"
_white = "\u001b[37m"
_green = "\u001b[32m"
_magenta = "\u001b[32m"
_cyan = "\u001b[36m"
_yellow = "\x1b[33;21m"
_red = "\x1b[31;21m"
_bold_red = "\x1b[31;1m"
_reset = "\x1b[0m"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {  # The formatter name, it can be anything that I wish
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(filename)s: %(funcName)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",  # How to display dates
        },
        "default_colored": {  # The formatter name, it can be anything that I wish
            "format": f"{_cyan}%(asctime)s{_reset} {_white}-{_reset} {_magenta}%(name)s{_reset} {_white}-{_reset} {_bold_red}%(levelname)s{_reset} {_white}-{_reset} {_blue}%(filename)s: %(funcName)s{_reset} {_white}-{_reset} {_cyan}%(message)s{_reset}",
            "datefmt": "%Y-%m-%d %H:%M:%S",  # How to display dates
        },
        "simple": {  # The formatter name
            "format": "%(message)s",  # As simple as possible!
        },
        "json": {  # The formatter name
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",  # The class to instantiate!
            # Json is more complex, but easier to read, display all attributes!
            "format": """
                    tags: %(tags)l
                    asctime: %(asctime)s
                    created: %(created)f
                    filename: %(filename)s
                    funcName: %(funcName)s
                    levelname: %(levelname)s
                    levelno: %(levelno)s
                    lineno: %(lineno)d
                    message: %(message)s
                    module: %(module)s
                    msec: %(msecs)d
                    name: %(name)s
                    pathname: %(pathname)s
                    process: %(process)d
                    processName: %(processName)s
                    relativeCreated: %(relativeCreated)d
                    thread: %(thread)d
                    threadName: %(threadName)s
                    exc_info: %(exc_info)s
                """,
            "datefmt": "%Y-%m-%d %H:%M:%S",  # How to display dates
        },
    },
    "filters": {
        "tagsDefault": {
            "()": "core.loger.DefaultFilter",
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "default_colored",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": f"{tempfile.mkdtemp(prefix='vendor.', suffix='.logs')}/vendor.log",
            "mode": "a",
            "maxBytes": 10485760,
            "backupCount": 5,
        },
        "logstash": {
            "formatter": "json",
            "level": "DEBUG",
            "class": "logstash_async.handler.AsynchronousLogstashHandler",
            "host": settings.LOGSTASH_HOST,
            "port": settings.LOGSTASH_PORT,  # Default value: 5959
            "version": 1,
            "transport": "logstash_async.transport.UdpTransport",
            # Version of logstash event schema. Default value: 0 (for backward compatibility of the library)
            "filters": ["tagsDefault"],
            "database_path": "",
        },
    },
    "loggers": {
        # "db": {"level": "DEBUG", "handlers": ["console"]},
        # "fastapi.request": {"level": "DEBUG", "handlers": ["console"]},
        "sqlalchemy.engine": {"level": "INFO", "propagate": 1},
        "": {"level": "DEBUG", "handlers": ["console", "file", "logstash"]},
    },
}
