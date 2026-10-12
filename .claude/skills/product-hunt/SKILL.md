---
name: product-hunt
description: Find new product candidates by sweeping Meta Ad Library at our price point, then put the survivors through the gates and into the workbook. Use when asked to find, hunt, source or research new products, or when the shortlist is too thin to choose from.
---

# Product hunt

Finds new candidates. Target **five survivors**, because realistically three
get tested to find one that works.

Read `CLAUDE.md` first. Budget roughly 30-45 minutes.

## The method: start from ads at our price point

**Do not start from viral Reels.** That was the old method and it wasted
effort: a product can have three million likes and still be unsellable
because eight advertisers have fixed its price at Rs 399. Price is the
binding constraint, so filter on it first.

A competing dropshipper carries our cost structure. What they charge is the
single most informative number available, and it is public.

### Step 1 — Sweep categories

Pick 5-8 product types fitting the hard filters in `PRODUCT-SELECTION.md`:
battery or USB (never mains), no warranty, not fragile, small and light,
plausible for a woman 25-45 buying for her home.

For each, open Ad Library and run `tools/browser/adlib_extract.js`:

```
https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=IN&q=<terms>&search_type=keyword_unordered&media_type=all
```

Keep a category when **priceMedian is at or above our floor** and there are
**>= 3 distinct advertisers**. Drop it immediately when the median sits below
the floor — that is an anchor we cannot beat, and it is what killed the
vegetable chopper, the mini sewing machine, the lint remover and the portable
blender.

Do not search by price ("Rs 999 COD"). It surfaces apparel. Search the
product type and read prices out of the ad copy.

### Step 2 — Supply-check the survivors

```
.venv/bin/python tools/deodap_lookup.py "<a>" "<b>" "<c>" --limit 2 --out data/catalog/deodap-<date>.csv
```

Batch them in one call; it paces itself politely. Anything absent from DeoDap
is dead regardless of how good the ad market looks.

### Step 3 — Gates 3 and 4, then economics

Run the survivors through `product-check` for the price anchor, perceived
value and unit economics. Price each at what it carries, not at the floor.

### Step 4 — Write everything down

**Every product found goes in the Candidates tab, including the rejects, with
its reason.** The record of what was rejected and why is as valuable as the
shortlist — the blocked ones are how we learned the price-anchor rule.

```
.venv/bin/python tools/sheet_sync.py push-candidates
.venv/bin/python tools/sheet_sync.py push-shortlist
```

Then write `research/pass-<date>-<topic>.md`: what was swept, the table of
advertisers / duration / prices / cost, what survived and what the pass
taught us about the market.

## Where the good categories are

Established by the 2026-10-12 sweep:

- **Home and kitchen gadgets cluster at Rs 299-999** and are mostly anchored
  below our floor. Expect a low hit rate here.
- **Wellness and personal care price far higher** — massage guns at a Rs 999
  median, neck massagers at Rs 2,399, same COD model and buyer.
- **Unfamiliar beats familiar.** Anything a buyer has already owned carries a
  price in their head. Gadgets do not.

Note the tension honestly when it arises: the niche on record is home decor
and organisation, and that is exactly where commodity pricing bites hardest.
Surface it as a decision for the owner rather than drifting out of the niche
without saying so.

## Report

A ranked table: product, advertisers, longest run, **what competitors
charge**, DeoDap cost and weight, our price, target CPP, verdict. Name one
recommendation and say why it beats the runner-up. Say plainly which gates
were not run.
