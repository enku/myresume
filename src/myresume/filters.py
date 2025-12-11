"""Template filters

These are Jinja2 template filters that can be used in theme templates.
"""

import re
from urllib.parse import unquote, urlparse


def regex_replace(string: str, pattern: str, replacement: str, count: int = 0) -> str:
    """Regex replace"""
    return re.sub(pattern, replacement, string, count)


def pretty_url(url: str, dash: str = "•") -> str:
    """Make url pretty by removing scheme, query strings, trailing slashes, etc

    In tel: URLs, replace dashes with `dash`.
    """
    parsed = urlparse(url)
    path = unquote(parsed.path).rstrip("/")

    address, colon, port = parsed.netloc.partition(":")

    if colon and (parsed.scheme, port) not in [("http", "80"), ("https", "443")]:
        address = f"{address}:{port}"

    if parsed.scheme == "tel":
        path = path.replace("-", dash)

    return f"{address}{path}"
