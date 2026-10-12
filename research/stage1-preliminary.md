# Stage 1 — Preliminary demand signal (incomplete)

**Date:** 2026-10-12
**Status:** PARTIAL. The two load-bearing sources — Google Trends and Meta
Ad Library — both need browser access, which is not yet enabled. Amazon
India returned HTTP 503 to a direct fetch. What follows is one vendor's
order data plus trend commentary, and is **not** sufficient to pick a
product.

## The one real data point found

Shiprocket is a courier aggregator, so its order counts are a genuine
demand proxy rather than marketing copy — though it publishes no
methodology, sample size or time period, and the article is dated
**13 May 2026** [source: shiprocket.in].

| Item / category | Orders |
|---|---|
| Boxes (subcategory) | 86,869 |
| Waterproof drawer liner | 8,589 |
| Fridge storage containers | top product, no count |
| Wardrobe organizers | top product, no count |
| Furniture organizers | strong, no count |

**Price bands:**

| Band | Orders |
|---|---|
| **Rs 500-1,000** | **42,506** |
| Rs 2,000+ | 22,500 |

**Monthly:** April 2026 peak at 54,771 orders, May 2026 down to 32,610.
April is not a festive month, so this is likely a home-improvement season
effect. Worth confirming against a full year before trusting it.

## This creates a real tension with our price floor

Our floor is Rs 1,099, set by ad-cost headroom: below it, Meta CPP in India
eats the product (`PLAN.md` §2). But the **highest-volume band in home
decor is Rs 500-1,000** — nearly double the Rs 2,000+ band.

Both facts can be true at once. The Rs 500-1,000 volume is probably
marketplace, organic and repeat demand, where there is no Rs 200-400
acquisition cost to cover. Paid-social acquisition cannot live there.

**Resolution: sell bundles that land at Rs 1,099-1,399, not single items
priced there.** A set of three at Rs 1,299 reads as Rs 433 per piece — inside
the market's comfort zone — while our AOV clears the floor. This is what
`tools/score_products.py` already does with `bundle_qty`, and this data is
the first evidence that it is the right call rather than a workaround.

Avoid single items priced at Rs 1,099+. That is where the volume is thinnest
and the buyer's price anchor works against us.

## Candidate categories emerging

Cross-referencing the above against our hard filters
(`PRODUCT-SELECTION.md`) — light, non-fragile, bundles naturally, solves a
storage problem:

1. **Waterproof drawer / shelf liners** — 8,589 orders on one SKU. Light,
   unbreakable, sold in multiples by nature, and films well as a
   before/after. Strongest lead so far.
2. **Fridge storage containers** — named a top product. Plastic, stackable,
   natural set of 4-6. Check fragility and shipping weight.
3. **Wardrobe organizers** — named a top product. Fabric, light, cheap to
   ship, strong visual transformation.
4. **Drawer dividers / organisers** — adjacent to the above, already
   passing our scorecard on the template data.

All four are *storage* rather than *decoration*. That matches the market
reports: small-space urban demand, space-saving and multifunctional
[source: imarcgroup, housiey]. It also suits us better, because storage
solves a stateable problem, which `RESEARCH-METHOD.md` Stage 2 requires and
"pretty" fails.

## What is still needed before any shortlist

- **Google Trends, India** — 90-day and 5-year curves per term. Blocked on browser.
- **Meta Ad Library, India** — ad age per candidate. The single strongest
  free validation signal. Blocked on browser.
- **Amazon India Best Sellers / Movers & Shakers** — blocked (503 on fetch);
  needs browser.
- **Marketplace undercut test** per candidate — needs browser.

## Sources

- [Shiprocket — home decor trends India](https://www.shiprocket.in/blog/home-decor-trends-india/) — order counts; no methodology stated
- [IMARC — India home storage market](https://www.imarcgroup.com/india-home-storage-market) — space-saving demand drivers
- [Housiey — Indian home decor trends 2026](https://housiey.com/blogs/10-home-decor-trends-taking-over-indian-homes-in-2026) — multifunctional furniture
- [Homelane — 2026 design ideas](https://www.homelane.com/design-ideas/?p=721075) — vertical storage in compact flats

All vendor or marketing content. Treated as leads, not measurements.
