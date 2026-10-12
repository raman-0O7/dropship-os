---
name: shortlist-status
description: Report where the dropshipping experiment currently stands - live candidates, votes cast, blocked products and what to do next. Use when asked for status, where things stand, what to test next, or to review the shortlist.
---

# Shortlist status

A two-minute brief for a decision maker. Read, do not write — except to pull
the latest votes.

## Gather

```
.venv/bin/python tools/sheet_sync.py check
.venv/bin/python tools/sheet_sync.py pull-shortlist
```

`pull-shortlist` overwrites `data/shortlist.csv` with what is actually in the
workbook, votes included. **Always pull before reasoning about votes** — the
humans edit the sheet directly and the local file goes stale.

Then read `data/shortlist.csv` and `data/candidates.csv`.

## Report

**1. Live candidates**, ranked, as a table: id, product, our price, what
competitors charge, DeoDap cost and weight, target CPP, and any gate not yet
run. A candidate with an unchecked price anchor is not really a candidate —
say so.

**2. Votes.** Who has voted, on what, and what is still waiting on them. If
both partners have voted and agree, say what that unblocks.

**3. Blocked, with the reason in one line each.** Keep these visible. They are
why the gates exist, and they stop products being re-proposed.

**4. One recommendation.** What to test first and why it beats the runner-up.
Name it; a survey of options is work handed back.

**5. What is actually outstanding.** Be specific and honest. Unchecked gates,
missing supplier data, decisions waiting on the owner. If there are too few
live candidates to choose from, say that plainly rather than presenting a thin
list as a shortlist.

## Standing context

- Build Oct-Nov 2026, **test in the January CPM trough**. Festive inflation
  runs 30-60%. The 90-day clock starts at the first ad rupee, not now, so
  research and build time is free.
- Hard cap Rs 15,000. Flag any recommendation that would breach it.
- Rs 1,099 is a **floor**, not a price. A pending recommendation to lower it to
  Rs 899 sits in `research/pass-2026-10-12-adlibrary-first.md` — it is the
  owner's call and should be raised, not silently applied.
- No spending authority, ever. Never place, raise or resume a campaign.

## Rules

Label every figure `[source: url]`, `[computed]` or `[estimate]`. Never invent
market data. Report against the written thresholds in `PLAN.md` — kill means
kill.
