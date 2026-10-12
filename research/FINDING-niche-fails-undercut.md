# Marketplace price gap — what it does and does not mean

> **CORRECTED 2026-10-12, same day.** The first version of this file
> concluded the niche was dead. That was wrong on two counts, and the
> owner was right to push back. Correction is at the bottom under
> "What this finding actually means". The price data below stands; the
> conclusion drawn from it did not.

**Date:** 2026-10-12 · **Method:** Amazon India + Meesho read directly in
browser. This is Stage 3 of `RESEARCH-METHOD.md`, the test that was never
run before today.

## The data

**Amazon India — Home Storage & Organisation bestsellers** (top 30)
[source: amazon.in/gp/bestsellers/kitchen/1380510031]

| Product | Price | Ratings |
|---|---|---|
| Homestrap saree cover / wardrobe organiser, set of 6 | **Rs 299** | 20,289 |
| Storite under-bed storage bag, 2-pack | **Rs 399** | 28,448 |
| amazon basics vacuum compression bags, 5-pack | **Rs 429** | 158,767 |
| SOLSTICE saree covers, set of 12 | Rs 589 | 5,063 |
| Adhesive wall hooks, 20 pcs | Rs 149-229 | 4,549-14,687 |
| Laundry basket, foldable | Rs 146 | 13,937 |

Range across the whole top 30: **Rs 94 - Rs 1,599**, with the great
majority under Rs 500. Eight of thirty entries are garbage bags.

**Amazon India — Home & Decor bestsellers** (top 30)
[source: amazon.in/gp/bestsellers/kitchen/1380374031]

Range: **Rs 76 - Rs 599.** Dominated by Diwali string lights (Rs 76-139),
air fresheners (Rs 97-199), tealight candles (Rs 299-349), wall clocks
(Rs 159-598).

**Meesho — "home organizer"** [source: meesho.com/search?q=home+organizer]

| Product | Price | Reviews |
|---|---|---|
| Trendy Makeup Vanity Box And Organizers | **Rs 174** | 8,390 |
| Makeup Vanity Box And Organizers | Rs 187-214 | 805-2,247 |
| Over the Door Shoe Organizers | **Rs 484** | 13,245 |
| Collapsible Shoe Racks | Rs 283 | 3,303 |
| Multipurpose decor basket, set of 3 | Rs 277 | 100 |

Range: **Rs 120 - Rs 939**, mostly Rs 150-480. "Makeup Vanity Box And
Organizers" is an entire Meesho category with thousands of reviews.

## What the first version claimed this killed

Our price floor is Rs 1,099, set by ad-cost headroom (`PLAN.md` §2). The
entire category transacts at **one fifth of that**, with 2-day delivery and
thousands of reviews as social proof.

Every lead from `stage1-demand.md` dies here:

| Lead | Killed by |
|---|---|
| Acrylic makeup / vanity organiser | Meesho Rs 156-214, 8,390 reviews |
| Wardrobe / closet organiser | Amazon Rs 299, 20,289 ratings |
| Under-bed storage with wheels | Amazon Rs 399, 28,448 ratings |
| Drawer organiser / divider sets | same commodity band |
| Waterproof drawer liner | already demoted on no search demand |

## Can a lower price rescue it? No.

Optimistic case — RTO 20% not 30%, prepaid share 40% via OTP and partial
COD, lighter Rs 60 shipping, COGS at 30% of SP [computed]:

| Selling price | Break-even CPP |
|---|---|
| Rs 599 | Rs 226 |
| Rs 699 | Rs 276 |
| Rs 799 | Rs 326 |
| Rs 899 | Rs 377 |

Against an India CPP of Rs 150-400, Rs 799-899 is arguably survivable. But
that is not the real problem. **The real problem is that a buyer who sees
our ad can find the same item on Meesho for Rs 200 in one search.** No
pricing strategy fixes that; it is a product-choice problem.

## The methodological error this exposes

`RESEARCH-METHOD.md` listed Amazon Best Sellers / Movers & Shakers as a
**primary idea source**. That is backwards.

Amazon's bestsellers are, by definition, **commoditised** products —
garbage bags, wall hooks, string lights. They are "I know what I need"
purchases, won on price and delivery speed. We cannot win either.

**Amazon and Meesho are the FILTER, not the SOURCE.** Their correct use is
to kill a candidate that is already commoditised. Ideas must come from
where products surface *before* commoditisation: Instagram Reels, Meta Ad
Library, and global leading indicators.

(Also noted: Amazon India does not populate Movers & Shakers for Home &
Kitchen at all — "no movers and shakers available in this category". The
guide that recommended it was written for Amazon US.)

## What we are actually looking for

Paid social sells **"I didn't know I wanted this."** The product must be:

1. **Not price-comparable** — novel, personalised, or not yet listed on
   marketplaces at scale.
2. **Naturally Rs 999-1,999**, so the economics close without a fight.
3. Light, non-fragile, strong visual transformation on video.

Commodity home storage fails 1 and 2 simultaneously. The niche choice is
the problem, not the execution.

## What this finding actually means — corrected

**Error 1: marketplace price does not cap our price.** We set our own
price. Plenty of Indian D2C brands sell at 3-5x the marketplace rate in the
same category and do fine, on branding, bundling, packaging and creative.
Nothing here forces us to Rs 299.

**Error 2: I compared category price BANDS, not like-for-like products.**
Those Rs 174 Meesho vanity boxes are small plastic boxes. A premium
multi-tier acrylic organiser set is a different product tier. I did not
check a single identical SKU before declaring the category dead. That is
the weaker half of this analysis and it should not have been written as a
conclusion.

### What the gap really does: it taxes conversion, and that is measurable

A visible cheaper alternative does not block the sale. It lowers the
conversion rate. And CPP = CPC / conversion rate, so conversion is what
actually decides whether we live.

At Rs 1,099 (break-even CPP Rs 416, target Rs 291) [computed]:

| CPC | CVR to break even | CVR to hit target |
|---|---|---|
| Rs 4 | 0.96% | 1.37% |
| Rs 6 | 1.44% | 2.06% |
| Rs 8 | 1.92% | 2.75% |
| Rs 10 | 2.40% | 3.44% |

Typical Indian COD store conversion is 1-3%. **Rs 1,099 needs 1.4-2.4%.
That is inside the normal band**, not outside it. The niche is constrained,
not dead.

### The corrected filter

Replace "available cheaper on a marketplace -> reject" with:

> Is the **identical** product available on Amazon/Flipkart/Meesho at a
> large multiple cheaper, with fast delivery and heavy social proof? If
> yes, and we have no differentiation story, the conversion tax is likely
> to push CPP past break-even. Reject.
>
> If the item is differentiated — a set not sold there, a design not
> available there, a problem the marketplace listing does not articulate —
> the gap is a creative problem, not a kill.

So the real question per candidate is not "is it cheaper elsewhere" but
**"can the ad justify the difference"**. That is what Stage 2's visual hook
and problem statement are for.

## Cost of this finding

Zero rupees. The price data is genuinely useful — it tells us the size of
the gap our creative has to overcome per candidate, which is exactly what
the scorecard needs. The overreach was the conclusion, not the research.
