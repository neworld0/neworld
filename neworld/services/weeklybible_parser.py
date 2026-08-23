import re
from dataclasses import dataclass
from datetime import timedelta
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from .wol_client import WolParseError, WolValidationError


@dataclass(frozen=True)
class ParsedWeeklyBible:
    year: int
    n_week: int
    week: str
    bible_range: str
    bible_link: str
    specific_id: str


def next_iso_week(value):
    monday = value - timedelta(days=value.weekday())
    iso = (monday + timedelta(days=7)).isocalendar()
    return iso[0], iso[1]


def parse_weeklybible(html, year, week, source_url):
    if not html or not html.strip():
        raise WolParseError("Empty meetings document")
    soup = BeautifulSoup(html, "html.parser")
    root = soup.select_one("#article")
    if root is None:
        raise WolParseError("Meetings article root is missing")
    candidates = []
    for header in root.select("header"):
        h1, h2 = header.find("h1"), header.find("h2")
        link = h2.find("a", href=True) if h2 else None
        if not (h1 and h2 and link):
            continue
        heading, bible_range = h1.get_text(" ", strip=True), h2.get_text(" ", strip=True)
        parsed = urlparse(urljoin("https://wol.jw.org", link["href"]))
        parts = [part for part in parsed.path.split("/") if part]
        specific_id = next((part for part in reversed(parts) if re.fullmatch(r"\d{6,}", part)), "")
        if parsed.hostname == "wol.jw.org" and heading and bible_range and specific_id:
            candidates.append((heading, bible_range, parsed._replace(query="", fragment="").geturl(), specific_id))
    if len(candidates) != 1:
        raise WolValidationError("Meeting candidate is missing or ambiguous")
    item = candidates[0]
    return ParsedWeeklyBible(year, week, item[0], item[1], item[2], item[3])
