#!/usr/bin/env python3
"""
myresume is a program to convert a resume definition in YAML to HTML or PDF.
"""
import datetime
import importlib.metadata
import io
import locale
from urllib.parse import urlparse

import slugify
import weasyprint
import weasyprint.text.fonts
from html2text import html2text
from jinja2 import Environment, PackageLoader, select_autoescape

from . import filters

# Current locale for "January"
JANUARY = locale.nl_langinfo(locale.MON_1)

# link schemes filtered out when not public
PRIVATE_URL_SCHEMES = ["tel"]


class Resume:
    """Resume object instantiated from a dict"""

    def __init__(self, struct: dict):
        self.context = struct.copy()

        if self.context["meta"]["since"] is not None:
            for section in self.context["sections"]:
                section["entries"], section["olderEntries"] = filter_dates(
                    section["entries"], self.context["meta"]["since"]
                )

        self.context["meta"]["myresume"] = {"version": version()}

        if self.context["meta"]["public"]:
            self._filter_private()

    def _filter_private(self):
        """Filter "private" data out of the resume struct"""
        context = self.context

        context["contactInfo"]["address"] = ""
        context["links"] = [
            link
            for link in context["links"]
            if urlparse(link["url"]).scheme not in PRIVATE_URL_SCHEMES
        ]

    def to_html(self, theme="default") -> str:
        """Return Resume as HTML"""
        env = Environment(
            loader=PackageLoader("myresume", f"themes/{theme}"),
            autoescape=select_autoescape(["html"]),
        )
        env.filters["regex_replace"] = filters.regex_replace
        env.filters["pretty_url"] = filters.pretty_url
        env.filters["slugify"] = slugify.slugify
        template = env.get_template("resume.html")

        return template.render(self.context)

    def __str__(self) -> str:
        return self.to_html()

    def to_pdf(self, theme="default", pagesize="Letter") -> bytes:
        """Return Resume as a PDF document"""
        html = weasyprint.HTML(string=self.to_html(theme))
        css = weasyprint.CSS(string=f"@page {{ size: {pagesize} }}")
        font_config = weasyprint.text.fonts.FontConfiguration()
        document = html.render(font_config=font_config, stylesheets=[css])
        target = io.BytesIO()

        document.write_pdf(target)

        return target.getvalue()

    def to_text(self, theme="default") -> str:
        """Return resume as (markdown) text"""
        html = self.to_html(theme)

        return html2text(html)


def filter_dates(entries: list, since: int):
    """Divide `entries` into "current" and "older" according to `since`"""
    from_date = datetime.date(year=since, month=1, day=1)

    divided: tuple[list, list] = ([], [])  # recent, older

    for entry in entries:
        ongoing = entry.get("to", "Present") == "Present"
        index = 0 if ongoing or to_date(entry["from"]) >= from_date else 1
        divided[index].append(entry)

    return divided


def to_date(date_spec: int | str) -> datetime.date:
    """Convert `date_spec` to datetime.

    `date_spec` must be either of the format:
        - Month Year (e.g. `"January 1969"`)
        - Year (e.g. `1969`)
    """
    date_str = str(date_spec)

    if " " not in date_str:
        # presume January
        date_str = f"{JANUARY} {date_str}"

    return datetime.datetime.strptime(date_str, "%B %Y").date()


def version() -> str:
    """Return the version of myresume"""
    return importlib.metadata.distribution("myresume").version
