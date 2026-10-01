"""Import spreadsheet rows as repository issues; stable IDs prevent reruns."""

import csv
import json
import os
from pathlib import Path
import sys
import time
import re
import urllib.error
import urllib.parse
import urllib.request


AREA_OPTIONS = {
    "Login",
    "Trip creation",
    "Ongoing trip",
    "Scheduled trip",
    "Alerts",
    "Reports",
    "Device or downlink",
    "Other",
}
REQUIRED_FIELDS = ("id", "title", "description", "area", "steps", "expected", "actual", "environment")
HEADER_ALIASES = {
    "id": {"id", "source bug id", "bug id", "issue id"},
    "title": {"title", "summary", "issue title"},
    "description": {"description", "desc", "details"},
    "area": {"area", "affected area", "module", "module page", "component"},
    "steps": {"steps", "steps to reproduce", "reproduce", "reproduction steps"},
    "expected": {"expected", "expected result", "expected behavior"},
    "actual": {"actual", "actual result", "actual behavior"},
    "evidence": {"evidence", "screenshots", "screenshots logs and trip or device id", "logs"},
    "environment": {"environment", "browser device", "platform"},
    "labels": {"labels", "label"},
    "assignees": {"assignees", "assignee", "owner"},
    "body": {"body", "issue body", "description and details"},
}
SECTION_ALIASES = {
    "description": {"description"},
    "area": {"affected area", "module page", "area"},
    "steps": {"steps to reproduce", "steps", "reproduction steps"},
    "expected": {"expected result", "expected behavior", "expected"},
    "actual": {"actual result", "actual behavior", "actual"},
    "evidence": {"evidence", "screenshots logs and trip or device id", "screenshots logs and trip device id"},
    "environment": {"environment", "browser device", "browser / device"},
}


def api(method, path, token, payload=None):
    url = "https://api.github.com" + path
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(url, data=data, method=method, headers={
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer " + token,
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "thinxfresh-issue-import",
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")[:1000]
        raise RuntimeError(f"GitHub API {exc.code}: {detail}") from exc


def rows_from(path):
    if path.suffix.lower() == ".csv":
        with path.open(encoding="utf-8-sig", newline="") as stream:
            yield from csv.DictReader(stream)
    elif path.suffix.lower() == ".xlsx":
        from openpyxl import load_workbook
        workbook = load_workbook(path, read_only=True, data_only=True)
        try:
            sheet = workbook.active
            iterator = sheet.iter_rows(values_only=True)
            headers = [str(value).strip() if value is not None else "" for value in next(iterator)]
            for values in iterator:
                yield dict(zip(headers, values))
        finally:
            workbook.close()
    else:
        raise ValueError("Use a .csv or .xlsx file")


def split_items(value):
    return [part.strip() for part in str(value or "").split(";") if part.strip()]


def normalized_header(value):
    return re.sub(r"\s+", " ", re.sub(r"[_/\\-]+", " ", str(value).strip().lower())).strip()


def extract_sections(body):
    sections = {}
    current = None
    values = []
    for line in str(body or "").splitlines():
        heading = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if heading:
            if current:
                sections[current] = "\n".join(values).strip()
            heading_name = normalized_header(heading.group(1))
            current = next((field for field, aliases in SECTION_ALIASES.items() if heading_name in aliases), None)
            values = []
        elif current:
            values.append(line)
    if current:
        sections[current] = "\n".join(values).strip()
    return sections


def canonicalize_row(raw):
    values = {}
    for key, value in raw.items():
        normalized = normalized_header(key)
        field = next((field for field, aliases in HEADER_ALIASES.items() if normalized in aliases), None)
        if field and str(value or "").strip():
            values[field] = str(value).strip()
    body_sections = extract_sections(values.get("body", ""))
    for field, value in body_sections.items():
        values.setdefault(field, value)
    return values


def infer_area(value, title, body):
    raw_area = str(value or "").strip()
    if raw_area in AREA_OPTIONS:
        return raw_area, ""
    text = f"{raw_area} {title} {body}".lower()
    matches = (
        ("login", "Login"),
        ("create trip", "Trip creation"),
        ("ongoing trip", "Ongoing trip"),
        ("scheduled trip", "Scheduled trip"),
        ("alert", "Alerts"),
        ("report", "Reports"),
        ("pdf", "Reports"),
        ("device", "Device or downlink"),
        ("tracker", "Device or downlink"),
    )
    for marker, area in matches:
        if marker in text:
            return area, raw_area
    return "Other", raw_area


def normalize_row(raw):
    row = canonicalize_row(raw)
    area, source_area = infer_area(row.get("area"), row.get("title", ""), row.get("body", ""))
    if source_area:
        source_note = f"Source area: {source_area}"
        row["evidence"] = "\n\n".join(part for part in (row.get("evidence", ""), source_note) if part)
    row["area"] = area
    missing = [field for field in REQUIRED_FIELDS if not row.get(field)]
    identity_missing = [field for field in ("id", "title") if field in missing]
    if identity_missing:
        raise ValueError(f"Row is missing required fields: {', '.join(identity_missing)}")
    if missing:
        placeholder = "Not provided in source export."
        for field in missing:
            row[field] = placeholder
        note = "Missing source fields: " + ", ".join(missing)
        row["evidence"] = "\n\n".join(part for part in (row.get("evidence", ""), note) if part)
    if "\n" in row["id"] or len(row["id"]) > 100:
        raise ValueError("id must be one line and <=100 characters")
    labels = split_items(row.get("labels")) or ["bug"]
    title = row["title"]
    if not title.startswith("[Bug] "):
        title = "[Bug] " + title
    return {
        "id": row["id"],
        "title": title,
        "description": row["description"],
        "area": row["area"],
        "steps": row["steps"],
        "expected": row["expected"],
        "actual": row["actual"],
        "evidence": row.get("evidence", ""),
        "environment": row["environment"],
        "labels": labels,
        "assignees": split_items(row.get("assignees")),
    }


def render_body(issue):
    sections = [
        ("Description", issue["description"]),
        ("Affected area", issue["area"]),
        ("Steps to reproduce", issue["steps"]),
        ("Expected result", issue["expected"]),
        ("Actual result", issue["actual"]),
        ("Screenshots, logs, and trip or device ID", issue["evidence"]),
        ("Environment", issue["environment"]),
    ]
    return "\n\n".join(f"## {heading}\n{value}" for heading, value in sections if value) + "\n"


def main():
    root = Path.cwd().resolve()
    path = (root / os.environ["INPUT_FILE"]).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError("Input file must be a committed file inside this repository")
    mode = os.environ.get("IMPORT_MODE", "preview")
    if mode not in ("preview", "create"):
        raise ValueError("Mode must be preview or create")
    repo = os.environ["GH_REPO"]
    token = os.environ["GH_TOKEN"]
    base = "/repos/" + "/".join(urllib.parse.quote(s, safe="") for s in repo.split("/"))
    if len(repo.split("/")) != 2:
        raise ValueError("Invalid GH_REPO")

    records = []
    seen = set()
    for line, raw in enumerate(rows_from(path), 2):
        row = {str(k).strip().lower(): str(v).strip() if v is not None else "" for k, v in raw.items() if k}
        if not any(row.values()):
            continue
        try:
            issue = normalize_row(row)
        except ValueError as error:
            raise ValueError(f"Row {line}: {error}") from error
        key = issue["id"]
        if key in seen:
            raise ValueError(f"Row {line}: duplicate id {key}")
        seen.add(key)
        records.append(issue)

    # List both open and closed issues. GitHub's issues endpoint also returns PRs.
    existing = set()
    page = 1
    while True:
        items = api("GET", f"{base}/issues?state=all&per_page=100&page={page}", token)
        for item in items:
            if "pull_request" in item:
                continue
            for line in (item.get("body") or "").splitlines():
                if line.startswith("<!-- spreadsheet-id: ") and line.endswith(" -->"):
                    existing.add(line[len("<!-- spreadsheet-id: "):-len(" -->")])
        if len(items) < 100:
            break
        page += 1

    created = skipped = 0
    for issue in records:
        key = issue["id"]
        if key in existing:
            print(f"SKIP {key}: issue already exists", flush=True)
            skipped += 1
            continue
        print(f"{'CREATE' if mode == 'create' else 'PREVIEW'} {key}: {issue['title']} labels={issue['labels']} assignees={issue['assignees']}", flush=True)
        if mode == "preview":
            continue
        marker = f"<!-- spreadsheet-id: {key} -->"
        payload = {"title": issue["title"], "body": f"{render_body(issue)}\n{marker}", "labels": issue["labels"]}
        if issue["assignees"]:
            payload["assignees"] = issue["assignees"]
        issue = api("POST", base + "/issues", token, payload)
        print(f"  {issue['html_url']}", flush=True)
        existing.add(key)
        created += 1
        time.sleep(1)
    print(f"Done: {len(records)} rows; {created} created; {skipped} skipped; mode={mode}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, RuntimeError, KeyError, StopIteration) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
