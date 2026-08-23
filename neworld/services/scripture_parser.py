import calendar
import re
from dataclasses import dataclass
from datetime import date
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .wol_client import WolParseError, WolValidationError

PLACEHOLDERS = {"데이터 준비 중", "data pending", ""}


@dataclass(frozen=True)
class ParsedScripture:
    source_date: date
    scripture_text: str
    body_text: str
    source_url: str


def _text(node):
    return "\n".join(filter(None, (line.strip() for line in node.get_text("\n").splitlines())))


def _block_date(block):
    values = [block.get("data-date", "")]
    values += [n.get("datetime", "") for n in block.select("time[datetime]")]
    values += [n.get_text(" ", strip=True) for n in block.select("time, .date, .day")]
    for value in values:
        match = re.search(r"(20\d{2})[-/.년\s]+(\d{1,2})[-/.월\s]+(\d{1,2})", value)
        if match:
            try:
                return date(*map(int, match.groups()))
            except ValueError:
                return None
    return None


def parse_scripture(html, target_date, source_url):
    if not html or not html.strip():
        raise WolParseError("Empty daily-text document")
    soup = BeautifulSoup(html, "html.parser")
    root = soup.select_one("#dailyText")
    if root is None:
        raise WolParseError("Daily-text root is missing")
    candidates = []
    for theme in root.select("p.themeScrp"):
        block = theme.find_parent(["article", "section", "div"])
        while block and block is not root and block.select_one("div.bodyTxt") is None:
            block = block.parent
        body = block.select_one("div.bodyTxt") if block else None
        if body is None:
            continue
        scripture_text, body_text = _text(theme), _text(body)
        if scripture_text.casefold() in PLACEHOLDERS or body_text.casefold() in PLACEHOLDERS:
            continue
        candidates.append((_block_date(block), scripture_text, body_text))
    matching = [item for item in candidates if item[0] == target_date]
    selected = matching[0] if len(matching) == 1 else candidates[0] if len(candidates) == 1 and candidates[0][0] is None else None
    if selected is None:
        raise WolValidationError("Daily-text candidates are missing, ambiguous, or date-mismatched")
    return ParsedScripture(selected[0] or target_date, selected[1], selected[2], source_url)

def parse_annual_scripture_link(html, year, list_url, month=None):
    """Find the selected year's daily-text document from WOL's annual list."""
    soup = BeautifulSoup(html, "html.parser")
    month_label = "%s\uc6d4" % month if month else ""
    for anchor in soup.find_all("a", href=True):
        text = anchor.get_text(" ", strip=True)
        is_daily_text = "\ub0a0\ub9c8\ub2e4 \uc131\uacbd\uc744 \uac80\ud1a0\ud568" in text
        is_target_month = bool(month_label and month_label in text)
        if ((is_daily_text and str(year) in text and (not month_label or is_target_month)) or
                is_target_month):
            return urljoin(list_url, anchor["href"])
    raise WolValidationError("Annual daily-text link is missing")


def _annual_date(value, default_year):
    match = re.search(r"(?:(20\d{2})\ub144\s*)?(\d{1,2})\uc6d4\s*(\d{1,2})\uc77c", value)
    if not match:
        return None
    year, month, day = match.groups()
    try:
        return date(int(year or default_year), int(month), int(day))
    except ValueError:
        return None


def parse_annual_scripture(html, target_date, source_url):
    """Extract one daily-text block from the annual WOL document."""
    soup = BeautifulSoup(html, "html.parser")
    paragraphs = soup.find_all("p")
    for index, heading in enumerate(paragraphs):
        if _annual_date(heading.get_text(" ", strip=True), target_date.year) != target_date:
            continue
        scripture_text = ""
        body_parts = []
        for paragraph in paragraphs[index + 1:]:
            if _annual_date(paragraph.get_text(" ", strip=True), target_date.year):
                break
            classes = paragraph.get("class", [])
            if "themeScrp" in classes:
                scripture_text = _text(paragraph)
            elif "sb" in classes:
                body_parts.append(_text(paragraph))
        body_text = "\n".join(part for part in body_parts if part)
        if (not scripture_text or not body_text or
                scripture_text.casefold() in PLACEHOLDERS or body_text.casefold() in PLACEHOLDERS):
            raise WolValidationError("Annual daily-text block is incomplete")
        return ParsedScripture(target_date, scripture_text, body_text, source_url)

    raise WolValidationError("Annual daily-text date is missing")


def parse_monthly_scriptures(html, year, month, source_url):
    """Extract every complete daily-text block for one month from saved WOL HTML."""
    if not html or not html.strip():
        raise WolParseError("Saved monthly document is empty")
    if not 1 <= month <= 12:
        raise WolValidationError("Month must be between 1 and 12")

    items = []
    for day in range(1, calendar.monthrange(year, month)[1] + 1):
        try:
            target_date = date(year, month, day)
        except ValueError:
            break
        try:
            items.append(parse_annual_scripture(html, target_date, source_url))
        except WolValidationError as exc:
            if "date is missing" in str(exc):
                continue
            raise
    if not items:
        raise WolValidationError("Saved monthly document has no complete daily-text blocks")
    if len(items) != calendar.monthrange(year, month)[1]:
        raise WolValidationError("Saved monthly document does not contain every date in the target month")
    return items


def parse_yearly_scriptures(html, year, source_url):
    """Extract every complete daily-text block for one calendar year."""
    if not html or not html.strip():
        raise WolParseError("Saved yearly document is empty")

    first_day = date(year, 1, 1)
    expected_days = 366 if calendar.isleap(year) else 365
    items = []
    for offset in range(expected_days):
        target_date = first_day.fromordinal(first_day.toordinal() + offset)
        try:
            items.append(parse_annual_scripture(html, target_date, source_url))
        except WolValidationError as exc:
            if "date is missing" in str(exc):
                continue
            raise
    if not items:
        raise WolValidationError("Saved yearly document has no complete daily-text blocks")
    if len(items) != expected_days:
        raise WolValidationError("Saved yearly document does not contain every date in the target year")
    return items


TEXT_DATE_PATTERN = re.compile(r"^.*?(\d{1,2})\uc6d4\s*(\d{1,2})\uc77c\s+(?:\uc6d4|\ud654|\uc218|\ubaa9|\uae08|\ud1a0|\uc77c)\uc694\uc77c$")


def parse_monthly_scripture_text(text, year, month, source_url):
    """Parse one month's plain-text Daily Text export."""
    if not text or not text.strip():
        raise WolParseError("Saved monthly text is empty")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    headings = [(index, TEXT_DATE_PATTERN.match(line)) for index, line in enumerate(lines)]
    headings = [(index, match) for index, match in headings if match]
    if not headings:
        raise WolValidationError("Saved monthly text has no dated entries")
    items = []
    for position, (index, match) in enumerate(headings):
        found_month, day = map(int, match.groups())
        if found_month != month:
            raise WolValidationError("Saved text contains a date from another month")
        try:
            target_date = date(year, found_month, day)
        except ValueError as exc:
            raise WolValidationError("Saved text has an invalid date") from exc
        next_index = headings[position + 1][0] if position + 1 < len(headings) else len(lines)
        content = lines[index + 1:next_index]
        if len(content) < 2:
            raise WolValidationError("Saved text has an incomplete daily-text block")
        items.append(ParsedScripture(target_date, content[0], "\n".join(content[1:]), source_url))
    expected_days = calendar.monthrange(year, month)[1]
    if len(items) != expected_days or {item.source_date.day for item in items} != set(range(1, expected_days + 1)):
        raise WolValidationError("Saved monthly text does not contain every date in the target month")
    return items


def parse_yearly_scripture_texts(monthly_texts, year, source_url):
    """Parse the 12 monthly text files from a yearly ZIP export."""
    if set(monthly_texts) != set(range(1, 13)):
        raise WolValidationError("Yearly ZIP must contain exactly the files for months 01 through 12")
    items = []
    for month in range(1, 13):
        items.extend(parse_monthly_scripture_text(monthly_texts[month], year, month, source_url))
    expected_days = 366 if calendar.isleap(year) else 365
    if len(items) != expected_days:
        raise WolValidationError("Saved yearly text does not contain every date in the target year")
    return items
