# Dropshipping Workspace — Context for every session

Read this before doing anything. It encodes decisions already made, so
they do not get re-litigated or quietly broken by a later session.

## The business

- **Niche:** home decor / home organisation, India, women 25-45.
  Constrained by marketplace price gaps, not ruled out — see the finding.
- **Supplier:** DeoDap.
- **Channel:** Meta (Instagram/Facebook Reels) -> Shopify store.
- **Status:** pre-launch capped experiment, started 2026-10-11.
- **Hard cap:** Rs 15,000 total. **Hard stop:** 90 days from the FIRST AD
  RUPEE, not from project start. Building costs no clock.

The owner is a developer with a full-time job. He is the **decision maker**,
not the operator: he will not do product research manually and will not
babysit ad campaigns. Claude does the research and analysis; he approves.

## My role

Third partner doing research and analysis. Concretely:
1. Source and score product candidates against the economics model.
2. Produce a per-product research brief with real figures.
3. Push shortlists to the shared Google Sheet for him and his partner to pick from.
4. Report on live campaigns and name a decision: scale / watch / kill.

## Decisions already made — do not reopen without new evidence

| Decision | Where the reasoning lives |
|---|---|
| Price floor Rs 1,099; target Rs 1,099-1,699 | `PLAN.md` §2 |
| Rs 1,099 is a FLOOR, not the price. Price each product at what it carries | `research/CORRECTION-floor-is-not-a-price.md` |
| NOT GST-registered; business is on the owner's own PAN | `PLAN.md` §2d |
| Never list on a marketplace while unregistered | `PLAN.md` §2d |
| Phase 1 plain COD + targeted prepaid offer; partial COD only after a winner | `PLAN.md` §2b |
| Ship COD non-responders, do not auto-cancel them | `AUTOMATION.md` |
| BUY a COD/OTP Shopify app, do not build one | `AUTOMATION.md` |
| Verify phone by OTP at checkout, not after the order | `AUTOMATION.md` |
| Kill at 2.5x break-even CPP with zero orders | `PLAN.md` §3 |
| Fragile materials (glass, ceramic, resin, marble) are excluded | `PRODUCT-SELECTION.md` |
| 13-KPI filter, must pass >=7; #3 margin and #4 proof near-mandatory | `KPI-SCORECARD.md` |
| Battery/USB OK, mains power NOT OK, no warranty on anything | `PRODUCT-SELECTION.md` |
| Every candidate goes in the Google Sheet with its source URL | `CLAUDE.md` "Knowledge base" |
| ONE workbook with tabs, written via the Sheets API; never recreate the file | `CLAUDE.md` "The workbook" |
| Demand research first, supplier catalog last | `RESEARCH-METHOD.md` |
| Competitor AD price is the real comparable - they share our cost structure | `research/pass-2026-10-12-adlibrary-first.md` |
| Search ads at our price point, not viral Reels, when hunting products | `research/pass-2026-10-12-adlibrary-first.md` |
| Long-running competitor ads are a BUY signal, not saturation | `RESEARCH-METHOD.md` §2 |
| ...but count ADVERTISERS, not ads; one advertiser runs 10+ ads per creative | `research/FINDING-price-anchor-vs-ad-proof.md` |
| Proof and price anchor are the same fact — check what competitors CHARGE | `research/FINDING-price-anchor-vs-ad-proof.md` |
| Shortlist gates: supply -> advertiser proof -> price anchor -> perceived value | `PRODUCT-SELECTION.md` |
| Competitor ADS anchor price (same feed); marketplace listings do not | `PRODUCT-SELECTION.md` Gate 4 |
| Block on recognisable-commodity, or retail <= our cost. NOT on a price multiple | `PRODUCT-SELECTION.md` Gate 4 |
| DeoDap is ONE supplier, not a marketplace: no sellers to rank, no order counts | `PRODUCT-SELECTION.md` |
| Do not test during festive CPM inflation; test in the January trough | `RESEARCH-METHOD.md` §0 |
| Buy no paid spy tools | `RESEARCH-METHOD.md` |
| Dummy Instagram account is the primary momentum source | `RESEARCH-METHOD.md` §1 |
| Amazon is a source ONLY past the branded top of a list; always undercut-check | `RESEARCH-METHOD.md` |
| DeoDap confirmed as supplier (Roposo Clout shut down Apr 2026) | `research/LEARNING-videos-2.md` |
| Never shortlist branded products | memory: product constraints |
| Marketplace price taxes CONVERSION, it does not cap our price | `research/FINDING-niche-fails-undercut.md` |
| Undercut test asks "identical item + no differentiation?", not "cheaper?" | `research/FINDING-niche-fails-undercut.md` |

## Knowledge base — this workspace IS the memory

The owner's standing instruction (2026-10-12): **everything learned in a
session must be written here**, so a later session loses nothing. That
means:

- Every product candidate goes in the Google Sheet **with its source URL**,
  so he can see exactly what I saw.
- Every research pass gets a dated file in `research/`.
- Every decision and every correction goes in the table above, with a
  pointer to where the reasoning lives.
- Corrections are written as corrections, not silent edits — the record of
  being wrong is part of the knowledge base.

Pipeline: **Candidates tab** (everything found) -> we shortlist together in
the **Shortlist tab** -> matched against the DeoDap catalog -> economics.

### The workbook — ONE file, one link, stable URL

https://docs.google.com/spreadsheets/d/19lBPIuiZN4krzYES2wqrGvViGXhXJ7v0LbCZUjg1FoY/edit

| Tab | Contents | Owner |
|---|---|---|
| `README` | what the workbook is, column ownership | Claude |
| `Candidates` | every product found: source URL, evidence, 13 KPI scores, total, status, reason. **Rejected products stay with their reason** — the record of what was rejected is as valuable as the shortlist. | Claude, replaced on each push |
| `Shortlist` | candidates that passed, both partners' votes, DeoDap match, cost and weight, computed economics, visual hook, undercut check | **Joint** |

**Never recreate this file.** Its ID is hardcoded in `tools/sheet_sync.py`.
Consolidated into one workbook on 2026-10-12 at the owner's request, so
there is a single link to share and a single permission to grant. The
separate shortlist spreadsheet (`1ADpsTsp...`) was superseded and its three
rows migrated; the owner deletes it manually, because the Drive connector's
write actions are blocked by the permission classifier.

### Writing to it

Use the Sheets API through the service account, **not** the Drive connector.
The connector's `update_file` is metadata-only (title and parent), so it can
create a sheet but cannot write a cell — that is why the log used to be
rebuilt at a new URL every time. That era is over.

```
.venv/bin/python tools/sheet_sync.py check              what the SA can see
.venv/bin/python tools/sheet_sync.py push-candidates    data/candidates.csv -> tab
.venv/bin/python tools/sheet_sync.py pull-shortlist     tab -> data/shortlist.csv
.venv/bin/python tools/sheet_sync.py push-shortlist     research columns only
```

Add `--dry-run` to any push first. Credential lives at
`~/.config/dropship/sheets-sa.json`, outside the repo, overridable with
`DROPSHIP_SA_KEY`. Service account: `sheet-writer@dropship-ops.iam.gserviceaccount.com`,
granted Editor on the workbook. Libraries are in `.venv` (gitignored).

**Column ownership in the Shortlist tab is enforced in code.**
`raman_vote`, `partner_vote`, `agreed`, `final_decision` and `decision_date`
are the humans' and `sheet_sync.py` will not write them under any flag; they
are shaded yellow in the sheet. Everything else is Claude's research output.
`push-shortlist` also never blanks a non-empty cell, never deletes a row, and
aborts outright if the header row has been reordered rather than risk writing
into the wrong column. Verified by a live clobber test on 2026-10-12.

Local mirrors: `data/candidates.csv` and `data/shortlist.csv`. The CSVs are
the version under version control; always `pull-shortlist` before reasoning
about votes, since the humans edit the sheet directly.

## Economics — never estimate these by hand

Always compute with the tools. They encode the India COD reality
(RTO, both shipping legs, COD fees, restocking loss).

```
.venv/bin/python tools/deodap_lookup.py "<product>" --limit 3   # REAL cost+weight
python3 tools/unit_economics.py --sp 1099 --cogs 122 --sensitivity
python3 tools/cod_policy.py    --sp 1099 --cogs 122
python3 tools/score_products.py data/catalog/<export>.csv
```

**Supplier costs are no longer a blocker.** DeoDap is a Shopify storefront
with public product data; `deodap_lookup.py` returns real cost, weight,
rating, review count and stock. Measured costs came in at Rs 74-200, far
under the Rs 280 we had been estimating — which moves target CPP from Rs 291
up to Rs 329-388 and gives the Rs 1,099 floor genuine headroom against the
Rs 200-250 CPP seen in practice. Never estimate a supplier cost again; look
it up.

Default assumptions: RTO 30% on plain COD, prepaid share 20%, shipping
Rs 70 each way, COD fee Rs 40, restock loss 15% of COGS. Revise these from
real order data once it exists, in one place: the tool defaults.

## Rules for my own output

- **Label every number.** Mark each figure `[source: <url or doc>]`,
  `[computed]`, or `[estimate]`. A research brief that mixes a real price
  with a guessed conversion rate and presents both flatly is worse than no
  brief, because it gets trusted.
- **Never hand-write a URL.** Copy it from tool output. DeoDap handles carry
  SKU prefixes and long tails that cannot be guessed from a title; six
  invented ones reached the sheet and all were 404s. `push-shortlist`
  HEAD-checks links and refuses to publish a dead one.
- **Never invent market data.** No made-up search volumes, competitor
  counts, CPMs or "trending" claims. If a figure cannot be sourced, say so
  and mark what it would take to get it.
- **Recommend one option, with the reason it beats the runner-up.** He is a
  decision maker; a survey of five choices is work handed back to him.
- **Report against the written thresholds**, not vibes. Kill means kill.

## Hard limits — not negotiable

- **No spending authority.** I never place, raise, or resume an ad campaign.
  Daily caps are set at the Meta platform level, not in our code.
- **No unsupervised customer messaging** beyond the fixed COD confirmation
  template.
- **No scraping that violates a site's terms.** If a data source needs
  terms-breaking access, say so and propose a legitimate alternative
  rather than quietly building a scraper.
- **Flag, don't absorb, a budget breach.** If a recommendation would push
  past the Rs 15,000 cap, say that explicitly.
- **Never write the humans' columns in the Shortlist tab.** Their votes and
  final decisions are theirs. `sheet_sync.py` enforces this; do not route
  around it.

## Skills — invoke these instead of improvising

| Command | Does |
|---|---|
| `/product-hunt` | Sweep Ad Library at our price point, gate the survivors, write them to the workbook. Target 5 keepers. |
| `/product-check` | One product through all four gates, with economics and a verdict. |
| `/shortlist-status` | Where things stand: live candidates, votes, blocked, one recommendation. |
| `/product-research` | Entry point — explains the flow and routes to the right one. |

Each encodes the corrections this project paid for. Prefer them to writing a
fresh procedure, and if one is wrong, fix the skill rather than working
around it in a single session.

## Layout

```
PLAN.md               the capped experiment: budget, sequence, kill rules
RESEARCH-METHOD.md    how product research is actually done here, w/ sources
PRODUCT-SELECTION.md  hard filters and scorecard for this niche
AUTOMATION.md         build order for the order/COD/reporting pipeline
SETUP.md              access and data still needed, with status
tools/                economics and scoring scripts
tools/sheet_sync.py   reads/writes the Google workbook (Sheets API)
data/candidates.csv   mirror of the Candidates tab
data/shortlist.csv    mirror of the Shortlist tab, votes included
data/catalog/         supplier catalog exports (input)
data/scored.csv       score_products.py output (gitignored, regenerable)
research/             one brief per researched product (output)
tools/browser/        JS snippets to paste into the browser tool
.claude/skills/       invokable procedures — see below
.venv/                gspread + google-auth (gitignored)
```
