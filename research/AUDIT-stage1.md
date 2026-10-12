# Audit trail — how the Stage 1 leads were produced

Written 2026-10-12 in response to "how exactly did you research this".
Every claim traced to the call that produced it, including the weak ones.

## Total work done

**Product research specifically** (excluding GST/WhatsApp/COD research):

| Action | Count | Result |
|---|---|---|
| Web searches | 2 | vendor blogs, weak |
| Page fetches | 3 | 1 returned HTTP 503 (amazon.in), 2 usable |
| Browser page loads | 4 | Google Trends x3, Meta Ad Library x1 |

That is roughly 30 minutes of a person's work. It is fast because reading
and cross-checking pages is fast, not because a shortcut was taken — but
it is **shallow relative to what `RESEARCH-METHOD.md` actually specifies.**
Stages 3 and 4 have not been run at all.

## Evidence chain, lead by lead

### Source A — Shiprocket blog (WEAK)

`shiprocket.in/blog/home-decor-trends-india/`, dated 13 May 2026. A courier
aggregator's own blog. No methodology, no sample size, no time period.

Produced:

| Lead | What the source actually said | Strength |
|---|---|---|
| Waterproof drawer liner | "8,589 orders" | a number, unverifiable |
| Boxes | "86,869 orders" | too generic to act on |
| Fridge storage containers | named a "top product", **no count** | just a vendor's list |
| Wardrobe organizers | named a "top product", **no count** | just a vendor's list |

So two of the four original leads rested on a vendor naming them with no
figure attached. That is barely evidence.

### Source B — Google Trends, India (STRONG)

Read directly in the browser, `geo=IN`. Three queries:

1. 12-month, 4 terms — gave the level/shape table
2. 5-year, 4 terms — gave the fad test
3. The Rising related-queries panel, for **"drawer organizer" only**

Query 3 is the single strongest source in this whole exercise. It is
Google's own data on what Indian users are searching more of, and it
produced the two leads that were not on my list:

- acrylic makeup organizer — Breakout
- under bed storage with wheels — Breakout
- closet organizers — +550%
- pegboard drawer organizer — +250%

**Limitation: I ran that panel for one term out of four.** The equivalent
panels for wardrobe organizer, fridge organizer and drawer liner were not
read. There may be better leads sitting in them.

### Source C — Meta Ad Library (PARTIAL)

One search: "makeup organizer", India, active ads, ~180 results. Scrolled
roughly three screens.

Recorded three start dates (22 Jun, 11 Jul, 3 Sep 2026) and a handful of
advertiser names. **That is not an ad-age distribution** — it is three
dates from the top of an impressions-sorted list, which biases toward big
spenders like Amazon.

The URL also carried `is_targeted_country=false`, so results were ads
*visible* in India, not India-targeted. A Pakistan advertiser appeared.

## How the ranking was actually decided

**By judgement, not by the scoring model.** `tools/score_products.py` has
not been run on any of these, because it needs supplier cost and weight and
we have no catalog data yet. So no unit economics exist for any lead.

The order came from three things, weighted by hand:

1. Breakout / rising status in Google Trends
2. Fit against the hard filters in `PRODUCT-SELECTION.md` (fragility, bulk)
3. Whether it targets women directly

That is a defensible heuristic. It is not a measurement, and it should not
be presented as one.

## What has NOT been done

- **Marketplace undercut test** — no Amazon/Flipkart/Meesho price or
  delivery-speed comparison for any lead. This kills candidates faster than
  anything else and is entirely unrun.
- **Ad Library for leads 2-4** — only "makeup organizer" was checked.
- **Rising-query panels for 3 of 4 terms.**
- **Unit economics** — zero. No supplier costs, so no CPP, no kill numbers.
- **Visual hook assessment** — `RESEARCH-METHOD.md` Stage 2 requires writing
  the second-1 and second-5 frames per product. Not done.
- **Acrylic durability** — gates the top lead entirely. Unchecked.
- **Amazon India Best Sellers** — HTTP 503, never retrieved.
- **Pinterest, Meesho, Flipkart, Instagram** — not opened.

## Honest status

What exists is **four leads with one strong source behind two of them**,
and no economics on any. `research/stage1-demand.md` says "Not yet a
shortlist" and that is accurate.

Calling these "selected products" would overstate it by a wide margin.
