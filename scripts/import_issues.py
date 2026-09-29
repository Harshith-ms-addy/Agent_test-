"""Import spreadsheet rows as repository issues; stable IDs prevent reruns."""
import csv
import json
import os
from pathlib import Path
import sys
import time
import urllib.error
import urllib.parse
import urllib.request


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
        key, title = row.get("id", ""), row.get("title", "")
        if not key or not title or "\n" in key or len(key) > 100:
            raise ValueError(f"Row {line}: id and title are required; id must be one line, <=100 characters")
        if key in seen:
            raise ValueError(f"Row {line}: duplicate id {key}")
        seen.add(key)
        records.append((key, title, row))

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
    for key, title, row in records:
        if key in existing:
            print(f"SKIP {key}: issue already exists", flush=True)
            skipped += 1
            continue
        labels = split_items(row.get("labels"))
        assignees = split_items(row.get("assignees"))
        print(f"{'CREATE' if mode == 'create' else 'PREVIEW'} {key}: {title} labels={labels} assignees={assignees}", flush=True)
        if mode == "preview":
            continue
        body = row.get("body", "").replace("\\n", "\n")
        marker = f"<!-- spreadsheet-id: {key} -->"
        payload = {"title": title, "body": f"{body}\n\n{marker}"}
        if labels:
            payload["labels"] = labels
        if assignees:
            payload["assignees"] = assignees
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
