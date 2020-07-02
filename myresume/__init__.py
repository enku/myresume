#!/usr/bin/env python3
import datetime
import locale
import subprocess
from urllib.parse import urlparse

from jinja2 import Environment, PackageLoader, select_autoescape

from . import filters


# Current locale for "January"
JANUARY = locale.nl_langinfo(locale.MON_1)

# link schemes filtered out when not public
PRIVATE_URL_SCHEMES = ["tel"]


class Resume:
    """Resume object instantiated from a dict"""

    def __init__(self, struct: dict):
        self.resume = struct.copy()

        if self.resume["meta"]["since"] is not None:
            for section in self.resume["sections"]:
                section["entries"], section["olderEntries"] = filter_dates(
                    section["entries"], self.resume["meta"]["since"]
                )

        if self.resume["meta"]["public"]:
            self._filter_private()

    def _filter_private(self):
        """Filter "private" data out of the resume struct"""
        resume = self.resume

        resume["contactInfo"]["address"] = ""
        resume["links"] = [
            link
            for link in resume["links"]
            if urlparse(link["url"]).scheme not in PRIVATE_URL_SCHEMES
        ]

    def to_html(self, theme="default") -> str:
        """Return Resume as html"""
        env = Environment(
            loader=PackageLoader("myresume", f"themes/{theme}"),
            autoescape=select_autoescape(["html"]),
        )
        env.filters["regex_replace"] = filters.regex_replace
        env.filters["pretty_url"] = filters.pretty_url
        template = env.get_template("resume.html")

        return template.render(self.resume)

    def __str__(self) -> str:
        return self.to_html()

    def to_pdf(self, theme="default", pagesize="Letter") -> bytes:
        """Return Resume as a PDF document"""
        html = self.to_html(theme)

        command = [
            "wkhtmltopdf",
            "--quiet",
            "--page-size",
            pagesize,
            "--print-media-type",
            "-",
            "-",
        ]
        process = subprocess.Popen(
            command, stdin=subprocess.PIPE, stdout=subprocess.PIPE
        )
        process.stdin.write(html.encode("utf-8"))
        process.stdin.close()
        pdf = process.stdout.read()
        process.stdout.close()
        process.wait()

        return pdf


def filter_dates(entries: list, since: int):
    """Divide `entries` into "current" and "older" according to `since`
    """
    from_date = datetime.date(year=since, month=1, day=1)

    divided = ([], [])  # recent, older

    for entry in entries:
        index = 0 if to_date(entry["from"]) >= from_date else 1
        divided[index].append(entry)

    return divided


def to_date(date_str: str) -> datetime.date:
    """Convert `date_string` to datetime.

    `date_string` must be either of the format:
        - Month Year (e.g. January 1969)
        - Year (e.g. 1969)
    """
    if " " not in date_str:
        # presume January
        date_str = f"{JANUARY} {date_str}"

    return datetime.datetime.strptime(date_str, "%B %Y").date()