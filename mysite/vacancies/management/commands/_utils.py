import hashlib
import urllib.parse as url_parser
from enum import Enum


class Colors(Enum):
    """
    Available colors.
    """
    RED = '\x1b[91m'
    GREEN = '\x1b[32m'
    END = '\x1b[0m'


def colorize(text: str, color: Colors) -> str:
    """
    Colorizing a text string.
    """
    return f"{color.value}{text}{Colors.END.value}"


def normalize_url(base, url):
    return url_parser.urljoin(base, url)


def url_to_md5(url):
    return hashlib.md5(url.encode()).hexdigest()


def debug_log(message):
    print(message)
    # with open('debug.log', 'a+') as _log_file:
    #     _log_file.write(f"{message}\n")


def error_log(message):
    print(message)
    # with open('error.log', 'a+') as _log_file:
    #     _log_file.write(f"{message}\n")
