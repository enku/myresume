"""Template filters

These are Jinja2 template filters that can be used in theme templates.
"""
from urllib.parse import urlparse, unquote
import re


def regex_replace(string: str, pattern: str, replacement: str, count: int = 0) -> str:
    """Regex replace"""
    return re.sub(pattern, replacement, string, count)


def pretty_url(url: str) -> str:
    """Make url pretty by removing scheme, query strings, trailing slashes, etc"""
    parsed = urlparse(url)
    path = unquote(parsed.path).rstrip("/")

    address, colon, port = parsed.netloc.partition(":")

    if colon:
        if (parsed.scheme == "http" and port == "80") or (
            parsed.scheme == "https" and port == "443"
        ):
            address = address
        else:
            address = f"{address}:{port}"

    if parsed.scheme == "tel":
        path = path.replace("-", "•")

    return f"{address}{path}"
