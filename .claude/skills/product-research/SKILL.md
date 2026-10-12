---
name: product-research
description: Entry point for product research on the dropshipping store - explains the flow and routes to the right skill. Use when asked about product research generally, or when unsure which research step applies.
---

# Product research — start here

Three skills do the work. Pick one:

| You want to | Use |
|---|---|
| Find new products | **product-hunt** |
| Vet one specific product | **product-check** |
| Know where things stand | **shortlist-status** |

Read `CLAUDE.md` before any of them.

## The flow in one page

```
product-hunt          sweep Ad Library at our price point, 5-8 categories
   |                  keep categories whose MEDIAN PRICE clears our floor
   v
product-check         four gates, cheapest first:
   |                    1. DeoDap supply exists      -> cost + weight + rating
   |                    2. >= 3 advertisers, >= 6 months
   |                    3. price anchor: is our price INSIDE theirs?
   |                    4. perceived value: can a buyer already price it?
   v
unit_economics.py     price at what it carries, not at the floor
   |                  target CPP must clear Rs 200-250
   v
sheet_sync.py         Candidates tab (everything, rejects included)
                      Shortlist tab (survivors; never touch the vote columns)
```

## What this project learned the hard way

Four corrections are baked into the gates above. A session that skips them
will repeat them.

1. **Count advertisers, not ads.** One advertiser runs ten ads from one
   creative. An ad count overstates competition tenfold.
2. **Long-running competitor ads are a BUY signal** — nobody pays Meta for
   twelve months to lose money. This is the opposite of the usual "avoid
   saturated niches" advice, and the opposite of what an earlier version of
   this file said.
3. **Proof and price anchor are the same fact.** Those twelve months also fix
   the price. For a commodity the second fact destroys the first. This blocks
   more products than every other gate combined.
4. **Marketplace price taxes conversion, it does not cap our price.** Charging
   more than Meesho is the business model. Block only on a recognisable
   commodity, or on retail sitting at or below our own supply cost.

## Tools

```
.venv/bin/python tools/deodap_lookup.py "<product>" --limit 3
python3          tools/unit_economics.py --sp <price> --cogs <cost> --sensitivity
python3          tools/cod_policy.py     --sp <price> --cogs <cost>
.venv/bin/python tools/sheet_sync.py check | pull-shortlist | push-shortlist | push-candidates
tools/browser/adlib_extract.js    paste into the browser JS tool on an Ad Library page
```

`tools/score_products.py` scores a bulk catalogue export to `data/scored.csv`.
It predates the four gates and does not apply them — treat its output as a
shortlist of things to run `product-check` on, never as a verdict.
