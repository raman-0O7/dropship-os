#!/usr/bin/env python3
"""Sync the local CSVs with the shared Google workbook.

Why this exists: the Drive connector Claude normally uses can create a Sheet
but cannot write cells into one, so the candidates log used to be rebuilt and
the old copy trashed, changing its URL every time. Worse, the shortlist could
not be filled in at all without destroying the votes in it. This script talks
to the Sheets API directly, so the workbook keeps one stable URL forever.

Everything lives in ONE workbook with one tab per purpose, so there is a single
link to share and a single permission to grant.

  README      what the workbook is and who owns which column
  Candidates  every product found. Entirely Claude's; replaced on each push.
  Shortlist   JOINT. Claude writes the research columns; the vote and decision
              columns belong to the humans and this script refuses to touch
              them. Enforced in code, not by good intentions.

Usage
  tools/sheet_sync.py check              report what the service account sees
  tools/sheet_sync.py init               create/rename the tabs, write README
  tools/sheet_sync.py push-candidates    data/candidates.csv -> Candidates tab
  tools/sheet_sync.py pull-shortlist     Shortlist tab -> data/shortlist.csv
  tools/sheet_sync.py push-shortlist     data/shortlist.csv -> Shortlist tab
                                         (research columns only)

Add --dry-run to any push to print what would change and write nothing.
Run with .venv/bin/python, or set DROPSHIP_SA_KEY to move the credential.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path

try:
    import gspread
    from google.oauth2.service_account import Credentials
except ImportError:
    sys.exit(
        "Missing libraries. Run:\n"
        "  python3 -m venv .venv && .venv/bin/pip install gspread google-auth\n"
        "then call this script with .venv/bin/python"
    )

REPO = Path(__file__).resolve().parent.parent
KEY_PATH = Path(
    os.environ.get("DROPSHIP_SA_KEY", "~/.config/dropship/sheets-sa.json")
).expanduser()
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# One workbook for everything. This ID is stable — never recreate the file.
WORKBOOK_ID = "19lBPIuiZN4krzYES2wqrGvViGXhXJ7v0LbCZUjg1FoY"
WORKBOOK_TITLE = "Dropshipping — Workspace"
WORKBOOK_URL = f"https://docs.google.com/spreadsheets/d/{WORKBOOK_ID}/edit"

TAB_README = "README"
TAB_CANDIDATES = "Candidates"
TAB_SHORTLIST = "Shortlist"

CANDIDATES_CSV = REPO / "data" / "candidates.csv"
SHORTLIST_CSV = REPO / "data" / "shortlist.csv"

# The Shortlist tab's columns, in order. Validated against row 1 before any
# write, so a reordered sheet aborts instead of writing into the wrong column.
SHORTLIST_COLUMNS = [
    # identity — enough to judge the product without opening the Candidates tab
    "id", "product", "category", "source", "source_url", "kpi_score",
    "why_it_made_the_list",
    # Claude's call, placed before the vote columns so it is read before voting
    "claude_rank", "claude_pick_reason",
    # the humans decide here
    "raman_vote", "tarun_vote", "agreed",
    # Meta Ad Library proof. Count ADVERTISERS, not ads: one advertiser often
    # runs 10 ads off a single creative, so an ad count overstates competition
    # by an order of magnitude. Duration is the real proof of profitability.
    "ad_advertisers", "ad_longest_run_months", "ad_market_price",
    "ad_price_range", "ad_advertisers_named", "ad_price_anchor_risk", "ad_url_1", "ad_url_2", "ad_url_3", "ad_checked",
    # What a buyer sees on a marketplace. This is the perceived-value anchor:
    # whether OUR price sits inside the range the buyer already knows.
    "market_median", "market_range", "market_multiple", "market_inside_range",
    "market_source", "market_checked",
    # DeoDap supply. Measured, not estimated.
    "deodap_found", "deodap_url", "deodap_cost", "deodap_weight_g",
    "deodap_rating", "deodap_reviews", "deodap_in_stock",
    # economics, computed by tools/unit_economics.py from the figures above
    "selling_price", "breakeven_cpp", "target_cpp", "kill_at_spend",
    # creative brief
    "visual_hook_sec1", "visual_hook_sec5", "problem_in_buyers_words",
    "verdict",
    # the humans decide here too
    "final_decision", "decision_date",
]

# Human territory. Claude never writes these, in any mode, ever.
HUMAN_COLUMNS = {
    "raman_vote", "tarun_vote", "agreed", "final_decision", "decision_date",
}

HEADER_FMT = {
    "textFormat": {"bold": True},
    "backgroundColor": {"red": 0.93, "green": 0.93, "blue": 0.93},
}
HUMAN_FMT = {
    "textFormat": {"bold": True},
    "backgroundColor": {"red": 1.0, "green": 0.95, "blue": 0.80},
}

README_ROWS = [
    ["Dropshipping — Workspace"],
    [],
    ["One workbook, one link. Tabs:"],
    [],
    ["Tab", "What it is", "Who owns it"],
    [TAB_CANDIDATES, "Every product found, with source URL, evidence and all 13 KPI scores. "
                     "Rejected products stay in the log with their reason.", "Claude — regenerated on each research pass"],
    [TAB_SHORTLIST, "Candidates that passed, where the two of you vote and the economics get filled in.",
                    "Joint — see the column split below"],
    [],
    ["Shortlist column ownership"],
    ["Yours (Claude will never write these)", ", ".join(
        c for c in SHORTLIST_COLUMNS if c in HUMAN_COLUMNS)],
    ["Claude's (research output)", ", ".join(
        c for c in SHORTLIST_COLUMNS if c not in HUMAN_COLUMNS)],
    [],
    ["Those columns are shaded yellow in the Shortlist tab. The sync script "
     "aborts if the header row is reordered, rather than writing to the wrong column."],
    [],
    ["Every figure is labelled [source: url], [computed] or [estimate]. "
     "An unlabelled number is a bug — tell Claude."],
    [],
    ["Synced by tools/sheet_sync.py in ~/coding/dropshipping-workspace."],
]


def client() -> gspread.Client:
    if not KEY_PATH.exists():
        sys.exit(f"No service account key at {KEY_PATH}")
    return gspread.authorize(
        Credentials.from_service_account_file(str(KEY_PATH), scopes=SCOPES)
    )


def book(gc: gspread.Client | None = None):
    return (gc or client()).open_by_key(WORKBOOK_ID)


def a1_col(idx0: int) -> str:
    """0-based column index -> A1 letter."""
    s, n = "", idx0 + 1
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def read_csv(path: Path) -> tuple[list[str], list[dict]]:
    if not path.exists():
        sys.exit(f"Missing {path}")
    with path.open(newline="", encoding="utf-8") as fh:
        rdr = csv.DictReader(fh)
        return list(rdr.fieldnames or []), list(rdr)


def sa_email() -> str:
    try:
        return json.loads(KEY_PATH.read_text()).get("client_email", "?")
    except Exception:
        return "?"


# --------------------------------------------------------------------- check

def cmd_check(_args) -> None:
    print(f"service account: {sa_email()}")
    try:
        sh = book()
    except Exception as exc:
        name = type(exc).__name__
        hint = (
            f"\n  Share the workbook with {sa_email()} as Editor."
            if "Permission" in name or "403" in str(exc) else ""
        )
        sys.exit(f"  FAIL cannot open the workbook: {name}{hint}")

    print(f"  OK   '{sh.title}'  {WORKBOOK_URL}")
    for ws in sh.worksheets():
        vals = ws.get_all_values()
        rows = max(len(vals) - 1, 0)
        print(f"       tab '{ws.title}' — {rows} data row(s), {ws.col_count} cols")
    missing = {TAB_README, TAB_CANDIDATES, TAB_SHORTLIST} - {w.title for w in sh.worksheets()}
    if missing:
        print(f"  note: missing tab(s) {sorted(missing)} — run: init")


# ---------------------------------------------------------------------- init

def cmd_init(args) -> None:
    sh = book()
    existing = {w.title: w for w in sh.worksheets()}
    print(f"workbook '{sh.title}' — tabs: {list(existing)}")

    if args.dry_run:
        print("  dry run — nothing written")
        return

    if sh.title != WORKBOOK_TITLE:
        sh.update_title(WORKBOOK_TITLE)
        print(f"  renamed workbook -> '{WORKBOOK_TITLE}'")

    # The original single tab holds the candidates data; adopt it by position
    # rather than creating a duplicate.
    if TAB_CANDIDATES not in existing:
        first = sh.get_worksheet(0)
        print(f"  renamed tab '{first.title}' -> '{TAB_CANDIDATES}'")
        first.update_title(TAB_CANDIDATES)
        existing[TAB_CANDIDATES] = first

    for title, rows, cols in ((TAB_SHORTLIST, 200, len(SHORTLIST_COLUMNS)), (TAB_README, 40, 4)):
        if title not in existing:
            existing[title] = sh.add_worksheet(title=title, rows=rows, cols=cols)
            print(f"  added tab '{title}'")

    # Shortlist header + the yellow shading that marks human columns.
    ws = existing[TAB_SHORTLIST]
    ws.update([SHORTLIST_COLUMNS], "A1")
    ws.freeze(rows=1, cols=2)
    last = a1_col(len(SHORTLIST_COLUMNS) - 1)
    ws.format(f"A1:{last}1", HEADER_FMT)
    for col in HUMAN_COLUMNS:
        letter = a1_col(SHORTLIST_COLUMNS.index(col))
        ws.format(f"{letter}1", HUMAN_FMT)
    print(f"  '{TAB_SHORTLIST}' header written, human columns shaded")

    # README
    rd = existing[TAB_README]
    rd.clear()
    width = max(len(r) for r in README_ROWS if r)
    rd.update([r + [""] * (width - len(r)) for r in README_ROWS], "A1")
    rd.format("A1", {"textFormat": {"bold": True, "fontSize": 14}})
    rd.format("A5:C5", HEADER_FMT)
    rd.format("A9", {"textFormat": {"bold": True}})
    print(f"  '{TAB_README}' written")

    # README first, then Candidates, then Shortlist.
    sh.reorder_worksheets([existing[TAB_README], existing[TAB_CANDIDATES], existing[TAB_SHORTLIST]])
    print(f"  done — {WORKBOOK_URL}")


# ---------------------------------------------------------- push candidates

def cmd_push_candidates(args) -> None:
    header, rows = read_csv(CANDIDATES_CSV)
    values = [header] + [[r.get(c, "") for c in header] for r in rows]
    print(f"{TAB_CANDIDATES}: {len(rows)} rows x {len(header)} cols from {CANDIDATES_CSV.name}")
    if args.dry_run:
        print("  dry run — nothing written")
        return

    ws = book().worksheet(TAB_CANDIDATES)
    ws.clear()
    ws.resize(rows=max(len(values), 2), cols=len(header))
    ws.update(values, "A1")
    ws.freeze(rows=1, cols=2)
    ws.format(f"A1:{a1_col(len(header) - 1)}1", HEADER_FMT)
    print(f"  written — {WORKBOOK_URL}")


# ----------------------------------------------------------- pull shortlist

def cmd_pull_shortlist(_args) -> None:
    values = book().worksheet(TAB_SHORTLIST).get_all_values()
    if not values:
        sys.exit(f"'{TAB_SHORTLIST}' is empty — run: init")
    header = values[0]
    _validate_header(header)

    SHORTLIST_CSV.parent.mkdir(parents=True, exist_ok=True)
    with SHORTLIST_CSV.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(values[1:])
    print(f"pulled {len(values) - 1} row(s) -> {SHORTLIST_CSV}")

    for row in values[1:]:
        rec = dict(zip(header, row))
        votes = " / ".join(
            f"{k.split('_')[0]}={rec.get(k) or '-'}" for k in ("raman_vote", "tarun_vote")
        )
        print(f"  {(rec.get('id') or '?'):<5} {(rec.get('product') or '')[:38]:<38} {votes}")


# ----------------------------------------------------------- push shortlist

def _validate_header(header: list[str]) -> None:
    got = [h.strip() for h in header[: len(SHORTLIST_COLUMNS)]]
    for i, exp in enumerate(SHORTLIST_COLUMNS):
        act = got[i] if i < len(got) else "<missing>"
        if exp != act:
            sys.exit(
                f"Shortlist header changed at column {a1_col(i)}: expected "
                f"'{exp}', found '{act}'. Refusing to write — fix the sheet or "
                f"update SHORTLIST_COLUMNS in {Path(__file__).name} first."
            )



def _verify_urls(local_rows: list[dict]) -> list[str]:
    """HEAD every URL about to be written. Returns a list of problems.

    This exists because six fabricated DeoDap URLs reached the Shortlist tab:
    handles typed from product titles rather than copied from the lookup
    tool's output. They looked right and every one was a 404. A URL is a
    claim like any other figure, so it gets checked before it is published.
    """
    import urllib.error
    import urllib.request

    # Meta rejects bot HEAD requests with 403 whatever the link; its ad
    # permalinks cannot be verified this way and are not worth failing on.
    unverifiable_hosts = ("facebook.com", "instagram.com")
    ua = {"User-Agent": "Mozilla/5.0"}
    problems, seen = [], {}
    for rec in local_rows:
        rid = (rec.get("id") or "?").strip()
        for col, val in rec.items():
            if not col.endswith("url") and not col.startswith("ad_url"):
                continue
            url = (val or "").strip()
            if not url.startswith("http"):
                continue
            if any(h in url for h in unverifiable_hosts):
                continue
            if url in seen:
                code = seen[url]
            else:
                try:
                    req = urllib.request.Request(url, headers=ua, method="HEAD")
                    code = urllib.request.urlopen(req, timeout=20).status
                except urllib.error.HTTPError as exc:
                    code = exc.code
                except Exception as exc:
                    code = type(exc).__name__
                seen[url] = code
            # 404/410 means the link is wrong. Anything else (403, 429, a
            # timeout) means the host would not answer us, which is not
            # evidence the link is broken.
            if code in (404, 410):
                problems.append(f"{rid}.{col}: HTTP {code} — {url}")
            elif code != 200:
                print(f"  note: could not verify {rid}.{col} (HTTP {code})")
    return problems


def cmd_push_shortlist(args) -> None:
    _, local_rows = read_csv(SHORTLIST_CSV)
    if not local_rows:
        sys.exit(f"{SHORTLIST_CSV} has no rows")

    ws = book().worksheet(TAB_SHORTLIST)
    sheet = ws.get_all_values()
    if not sheet:
        sys.exit(f"'{TAB_SHORTLIST}' is empty — run: init")
    _validate_header(sheet[0])

    row_of = {r[0].strip(): i + 2 for i, r in enumerate(sheet[1:]) if r and r[0].strip()}
    writable = [c for c in SHORTLIST_COLUMNS if c not in HUMAN_COLUMNS]

    updates, appends, touched = [], [], []
    for rec in local_rows:
        rid = (rec.get("id") or "").strip()
        if not rid:
            continue
        if rid in row_of:
            rownum = row_of[rid]
            row = sheet[rownum - 1]
            for col in writable:
                val = (rec.get(col) or "").strip()
                if not val:
                    continue  # never blank a cell that already holds something
                idx = SHORTLIST_COLUMNS.index(col)
                cur = row[idx] if idx < len(row) else ""
                if cur.strip() != val:
                    updates.append({"range": f"{a1_col(idx)}{rownum}", "values": [[val]]})
                    touched.append(f"{rid}.{col}")
        else:
            appends.append([
                "" if c in HUMAN_COLUMNS else (rec.get(c) or "") for c in SHORTLIST_COLUMNS
            ])

    if not args.skip_url_check:
        problems = _verify_urls(local_rows)
        if problems:
            print("Dead or unreachable URLs — refusing to publish:")
            for p in problems:
                print(f"  {p}")
            sys.exit(
                "Fix them (real handles are in data/catalog/deodap-matches*.csv), "
                "or pass --skip-url-check if a host is merely down."
            )
        print(f"  url check: all links resolve")

    print(f"{TAB_SHORTLIST}: {len(updates)} cell(s) to update, {len(appends)} row(s) to add")
    for t in touched:
        print(f"  ~ {t}")
    for a in appends:
        print(f"  + {a[0]} {a[1][:38]}")
    print(f"  protected, never written: {', '.join(sorted(HUMAN_COLUMNS))}")

    if args.dry_run:
        print("  dry run — nothing written")
        return
    if not updates and not appends:
        print("  already in sync")
        return
    if updates:
        ws.batch_update(updates, value_input_option="USER_ENTERED")
    if appends:
        ws.append_rows(appends, value_input_option="USER_ENTERED")
    print(f"  written — {WORKBOOK_URL}")


def main() -> None:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = p.add_subparsers(dest="cmd", required=True)
    for name, fn, dry in (
        ("check", cmd_check, False),
        ("init", cmd_init, True),
        ("push-candidates", cmd_push_candidates, True),
        ("pull-shortlist", cmd_pull_shortlist, False),
        ("push-shortlist", cmd_push_shortlist, True),
    ):
        sp = sub.add_parser(name, help=fn.__doc__)
        if dry:
            sp.add_argument("--dry-run", action="store_true")
        if name == "push-shortlist":
            sp.add_argument("--skip-url-check", action="store_true",
                            help="publish without HEAD-checking every link")
        sp.set_defaults(func=fn, dry_run=False, skip_url_check=False)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
