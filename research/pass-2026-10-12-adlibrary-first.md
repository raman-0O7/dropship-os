# Research pass: searching ads at our price point instead of viral Reels

Date: 2026-10-12. Owner's instruction: *"please check on how much money the
sellers are selling it because that is the real metrics that might relate to
us much more."* Correct, and it changed the method.

## Why competitor ad price beats marketplace price

A competing dropshipper has **our** cost structure: same DeoDap-type supply,
same COD, same RTO, same Meta CPM. What they charge is what the market clears
at for someone standing where we stand. A Meesho wholesaler's price is not
comparable; a dropshipper's ad is.

So the method inverts. Instead of finding viral products and then checking
whether we can price them, **start from what dropshippers advertise**, and
keep the ones whose price band contains ours.

## What the sweep found

Every row [source: Meta Ad Library, India, 2026-10-12]; costs
[source: deodap.in, same day].

| Product | Advertisers | Oldest ad | They charge | DeoDap cost | Verdict |
|---|---|---|---|---|---|
| **Massage gun** | 14 | 6 mo | **Rs 699 - 1,199** (med 999) | Rs 199 / 370g | **LIVE** |
| **Neck massager** | 9 | 3 mo | **Rs 999 - 6,999** (med 2,399) | Rs 1,059 / 962g | **LIVE** |
| Mini sewing machine | 13 | 11 mo | Rs 299 - 930 (med 299) | Rs 178 / 93g | blocked |
| Lint remover | 6 | 21 mo | Rs 449 - 599 | - | blocked |
| Portable blender | 6 | 16 mo | Rs 499 - 1,000 (med 499) | Rs 259 / 3.76 stars | blocked |
| Vegetable chopper (C018) | 8 | 13 mo | Rs 399 | Rs 122 / 495g | blocked |

## The structural finding

**Indian dropshipping in home and kitchen clusters at Rs 299-999.** Five of
six categories are anchored below our Rs 1,099 floor, including the mini
sewing machine, which has the single best supply signal we have seen
(1,907 DeoDap reviews, 93g) and is still unusable because thirteen
advertisers sell it at Rs 299.

This is not bad luck in product selection. **Our price floor sits above the
band this market operates in.** That is why only one of twenty-two candidates
survived.

Two ways out, and we found both:

1. **Categories that price higher.** Wellness does: massage guns at a
   Rs 999 median, neck massagers at Rs 2,399. Same COD model, same buyer
   profile, four to eight times the price of a chopper.
2. **Lower our floor.** See below.

## The floor should probably move to Rs 899

Rs 1,099 was derived when we assumed COGS of Rs 280. Measured costs are
Rs 74-200. Recomputed at the real figure [computed, COGS Rs 159]:

| Selling price | Break-even CPP | Target CPP |
|---|---|---|
| Rs 799 | Rs 307 | Rs 215 |
| **Rs 899** | **Rs 371** | **Rs 259** |
| Rs 1,099 | Rs 497 | Rs 348 |

Real Indian CPP is Rs 200-250. At Rs 899 the target of Rs 259 clears the top
of that band, which is the test the floor was built to enforce. The old
Rs 899 rejection assumed a cost we no longer pay.

Dropping the floor to Rs 899 puts us inside the Rs 699-1,199 band where much
of this market actually trades, instead of permanently above it.
**Recommendation for the owner to decide**, not a change I have made.

## Live shortlist after this pass

| rank | id | product | our price | competitors charge |
|---|---|---|---|---|
| 1 | C016 | USB garlic chopper | Rs 1,299 | no advertiser states a price |
| 2 | C023 | Massage gun | Rs 999 | Rs 699 - 1,199 |
| 3 | C017 | Silicone stretch lids | Rs 1,199 | not yet checked |
| 4 | C024 | Neck massager | Rs 2,399 | Rs 999 - 6,999 |

C023 is the first candidate whose price sits **inside** what competitors
already charge rather than above it. Every blocked product in this project
failed on exactly that gap.

## Method notes

- Price-first queries ("Rs 999 COD") surface apparel, not home goods. Search
  the product type and read the prices out of the ad copy instead.
- Extract per ad: advertiser, start date, every rupee figure in the body.
  Count distinct advertisers; a single advertiser's "10 ads use this creative"
  is one competitor, not ten.
- The ad-copy price is often absent. C016's six advertisers state no price at
  all, which is itself informative: nobody has planted a number.
- DeoDap advertises in the massager category directly. Our supplier competes
  with us.
