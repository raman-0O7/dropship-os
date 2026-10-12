---
name: product-check
description: Run one product through all four shortlist gates - DeoDap supply, competitor ad proof, price anchor, perceived value - and produce a verdict with real numbers. Use when asked to check, vet, validate or price a specific product, or to decide whether something belongs on the shortlist.
---

# Product check

One product in, one verdict out, every number measured. Takes about five
minutes. Read `CLAUDE.md` first for economics defaults and hard limits.

**Run the gates in this order.** They are sorted cheapest-and-most-absolute
first, so most rejects cost one command.

## Gate 1 — Supply exists

```
.venv/bin/python tools/deodap_lookup.py "<product>" --limit 3
```

Returns real cost, weight, rating, review count and stock. **Try at least
three phrasings** before concluding it is absent — C001 looked present until
four phrasings all returned lid knobs instead of handles.

- Not in the catalogue -> **STOP. Rejected.** No supply, no product,
  whatever the KPI score.
- Rating below 4.4, or fewer than 100 reviews -> flag as an RTO risk. On COD
  a weak product rating becomes refusals.

Record `deodap_cost`, `deodap_weight_g`, `deodap_rating`, `deodap_reviews`,
`deodap_in_stock`, `deodap_url`.

DeoDap is a **single supplier, not a marketplace**: no competing sellers to
rank, no public inventory, no order counts. Do not go looking for them.

## Gate 2 — Competitor ad proof

Open Meta Ad Library:

```
https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=IN&q=<product+terms>&search_type=keyword_unordered&media_type=all
```

Run `tools/browser/adlib_extract.js` through the browser JavaScript tool.

**Count advertisers, never ads.** One advertiser routinely runs ten ads from
one creative. Exclude national brands, marketplace affiliates (Meesho,
Flipkart, Wishlink creators) and copy aimed at another country — the India
filter leaks.

Pass mark: **>= 3 distinct advertisers, >= 1 running >= 6 months.** Do not
use a flat ad count; 10-15 ads can be one seller testing creatives.

Store up to three permalinks (`https://www.facebook.com/ads/library/?id=<ID>`).
They are the raw material for our own creatives later.

## Gate 3 — Price anchor (the one that bites)

From the same extract, read `priceLow`, `priceMedian`, `priceHigh`. **This is
the most important number in the whole check**: a competing dropshipper
carries our cost structure, so what they charge is what the market clears at
for someone standing where we stand.

- Our intended price **inside** their range -> **pass**. No price objection to
  overcome.
- Our price **above** their range on an undifferentiated item -> **blocked**.
  C018 had thirteen months of proof and eight advertisers, all at Rs 399, and
  is unsellable because of it.
- **No advertiser states a price** -> noteworthy and good: nobody has planted
  a number. Record it as such rather than leaving the field blank.

A HIGH anchor clears only with real differentiation: a bundle nobody else
sells, personalisation, or a segment the incumbents miss. Better creative is
not differentiation.

## Gate 4 — Perceived value

Could a typical buyer guess this item's price within about 30% before the
video starts?

- **Recognisable commodity** (masala box, storage basket, spice jars) ->
  **blocked**. No creative argues someone out of a price they already know.
- **Marketplace retail at or below our DeoDap cost** -> **blocked outright**.
  Arithmetic, not positioning. C021 retails near its own supply cost.
- Otherwise record the marketplace median and range as a **soft signal** — a
  conversion tax, not a cap. Marketplace price does not cap our price; use
  Amazon or Flipkart in preference to Meesho, which is the bargain end.

## Economics

```
python3 tools/unit_economics.py --sp <price> --cogs <deodap_cost> --sensitivity
python3 tools/cod_policy.py     --sp <price> --cogs <deodap_cost>
```

Price the product at **what it can carry**, not at the floor. Rs 1,099 is a
floor; the band is Rs 1,099-1,699 and anything above it is an explicit
exception needing its own RTO assumption (use `--rto 0.45` above Rs 1,500).

Sanity check: target CPP must clear **Rs 200-250**, the real Indian CPP at
this AOV. A target below that means the product loses money at a price buyers
accept, however good the rest looks.

## Write it down

Add or update the row via `data/shortlist.csv`, then:

```
.venv/bin/python tools/sheet_sync.py push-shortlist --dry-run
.venv/bin/python tools/sheet_sync.py push-shortlist
```

Never write `raman_vote`, `tarun_vote`, `agreed`, `final_decision` or
`decision_date` — the script refuses, and so should you.

Fill `claude_rank` and `claude_pick_reason`. The reason must say why this
product beats **the specific runner-up**, not why it is nice.

## Output to the owner

Verdict, the three or four numbers behind it, and one named recommendation.
Label every figure `[source: url]`, `[computed]` or `[estimate]`. If a gate
was not run, say so explicitly — an unchecked gate is the risk that has
blocked four products so far.

## Never hand-write a URL

Copy the `url` field from `deodap_lookup.py` output verbatim. Do **not**
construct a handle from the product title — DeoDap handles carry SKU prefixes
and long tails (`2118-silicone-lid-set-silicon-lids-for-containers-...`,
`0065-manual-stainless-...`) that are unguessable. Six invented URLs reached
the sheet this way and every one was a 404.

`push-shortlist` now HEAD-checks every link and refuses to publish on a
404/410. A URL is a claim like any other figure: `[source: url]` means the
URL was observed, not inferred.
