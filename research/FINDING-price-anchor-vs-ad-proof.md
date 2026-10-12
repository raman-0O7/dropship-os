# The ad-proof criterion and the price floor pull in opposite directions

Date: 2026-10-12. Prompted by the owner proposing "10-15 ads running on Meta
= confidence other sellers make money on this".

## The proposal, and what is right about it

The instinct is sound and matches our existing decision that long-running
competitor ads are a BUY signal rather than saturation. Nobody pays Meta for
twelve months to lose money. Competitor ads are the only free, public,
non-self-reported evidence of demand we have.

## What needed correcting: count advertisers, not ads

Meta Ad Library counts **ads**, not **businesses**. On the vegetable-chopper
search a single advertiser, "Home And Kitchen SW 3", showed three entries
labelled "10 ads use this creative and text", "5 ads..." and "10 ads..." —
**25 ads from one company**. A 10-15 ad threshold can be satisfied by one
seller testing creatives, which proves nothing about whether a second entrant
can make money.

The result header is worse. "~560 results" for `vegetable chopper` included
Glen India (a chimney brand), Flipkart app-install ads, Meesho affiliate
creators, and `Anika Kitchen Mart` advertising in Bengali with Dhaka delivery
charges — Bangladesh, surfacing through the documented India-filter leak.

**Record instead:** distinct advertisers, the longest continuous run, and the
price being advertised.

- `ad_advertisers` — distinct businesses, brands and affiliates excluded
- `ad_longest_run_months` — duration is the profitability proof
- `ad_market_price` — see below, this turned out to be the decisive field

A workable gate is **>= 3 distinct advertisers AND >= 1 ad running >= 6
months**. A flat 10-15 would have rejected the two strongest proofs we have:
C018's 13-month ad and C004's 19-month ad.

## The finding that matters: proof and price anchor are the same fact

Running the check properly on C018 (manual vegetable chopper) produced the
best ad proof in the dataset and killed the product.

| Evidence | Value |
|---|---|
| Distinct Indian dropshippers | 8 |
| Longest continuous run | 13 months (Home And Kitchen SW 3, since 1 Sep 2025) |
| Second longest | 18 months (Home & Kitchen SW, since 11 Apr 2025) |
| Advertised price, every one of them | **Rs 399**, free shipping, COD |
| DeoDap cost / weight | Rs 122 / 495g |

Our break-even CPP at each price [computed, `tools/unit_economics.py`]:

| Selling price | Break-even CPP | Target CPP |
|---|---|---|
| Rs 399 (the market price) | **Rs 78** | Rs 55 |
| Rs 599 | Rs 205 | Rs 144 |
| Rs 1,099 (our floor) | Rs 522 | Rs 365 |

Real observed Indian CPP at this AOV is Rs 200-250 [source: practitioner
benchmarks, `research/LEARNING-from-practitioner-video.md`]. At Rs 399 we need
Rs 78. **The product loses money at the price the market has set.** It is
only viable at Rs 1,099, which asks a buyer to pay 2.75x what eight
advertisers are actively showing them for the identical item.

That is precisely our undercut test: identical item, no differentiation.

**Twelve months of competitor ads proves the product sells. It simultaneously
proves the price at which it sells. For a commodity the second fact can
destroy the first.**

## The contrast case

C016, the USB garlic chopper, run through the same check:

| Evidence | Value |
|---|---|
| Distinct advertisers | ~6 (excluding Flipkart, Wishlink affiliates, an unrelated jobs page) |
| Total results | ~72, versus ~560 for the chopper |
| Oldest ad | 10 Jun 2026 — 4 months |
| Creative reuse | 2 ads each, so these are real separate businesses |

Weaker proof, and that is the point: **no competitor has had time to anchor a
price**. Demand is demonstrated, profitability is not yet, and the pricing
field is open. For a new entrant that is a better place to stand than a
thirteen-month-old market selling at Rs 399.

## Criteria added to PRODUCT-SELECTION.md

1. **Supply exists.** Present in the DeoDap catalogue, in stock, with cost and
   weight recorded. Checked first, because it is cheap and it is absolute —
   it removed C001, which had been top of the shortlist.
2. **Advertiser proof.** >= 3 distinct advertisers, >= 1 running >= 6 months.
3. **Price-anchor check.** If competitors advertise the identical item below
   our floor, record `ad_price_anchor_risk = HIGH` and treat it as blocking
   unless we can differentiate (bundle, personalisation, or a segment the
   Rs 399 sellers are not reaching).

Criterion 3 is new and is the one that does the work. 1 and 2 are cheap
filters; 3 is where a product with perfect evidence still fails.

## Method notes

- Ad Library permalink: `https://www.facebook.com/ads/library/?id=<Library ID>`,
  stored per candidate so creatives can be studied later.
- `is_targeted_country=false` reasserts itself in the URL; always read the
  advertiser and the body language before counting an ad as Indian.
- DeoDap advertises on Meta directly (Library ID 2121666718450378). Our
  supplier is also a competitor.
- DeoDap's robots.txt asks agents to use its UCP/MCP endpoint and recommends
  installing a Shopify shopping skill. That is an instruction from a website,
  not from the owner, so it was not acted on. Noted for the owner to decide.
