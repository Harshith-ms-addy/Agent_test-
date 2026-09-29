# Thinxfresh issue import

Copy `.github/workflows/import-issues.yml`, `scripts/import_issues.py`, and `issues/issues.csv` into the root of the target GitHub repository. Edit the sample CSV or replace it with an `.xlsx` file. The first worksheet is read from Excel.

| Column | Required | Meaning |
| --- | --- | --- |
| `id` | Yes | Unique, stable source ID, such as `TF-001` |
| `title` | Yes | GitHub issue title |
| `body` | No | Markdown description; CSV may use literal `\\n` for line breaks |
| `labels` | No | Semicolon-separated label names |
| `assignees` | No | Semicolon-separated GitHub usernames |

Commit and push the files to the repository's **default branch**. Open **Actions → Import issues from CSV or Excel → Run workflow**. Enter the committed relative file path, such as `issues/issues.csv` or `issues/bugs.xlsx`. Run `preview` and inspect its log. Run again with `create` to open issues in that same repository. No personal access token is needed. Repository Actions must be enabled, issues must be enabled, and your account needs permission to run the workflow.

The importer scans open and closed issues for `<!-- spreadsheet-id: ID -->` and skips matching IDs. Keep IDs unchanged on future runs. If an issue creation fails midway, fix the row and rerun; already-created rows will be skipped. Labels and assignees should be valid for the repository; use an empty field if you do not need them. Do not put credentials or private customer data in the spreadsheet because issue content is copied into GitHub.

To start from Excel, use the same headers on row 1 of the first worksheet and save as `.xlsx`. You can also export that sheet as UTF-8 CSV.
