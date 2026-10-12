# Correction: I treated the price floor as if it were the price

Date: 2026-10-12. Raised by the owner: *"why are we targeting a specific
1099 price?? If the product is good then we might sell it at higher price
right."* He is correct and the error was mine.

## What I got wrong

`PLAN.md` §2 says **"Price floor Rs 1,099; target Rs 1,099-1,699"**. A floor
and a band. I then computed every single product at exactly Rs 1,099 and, on
that basis, wrote that C021 was *"Rs 911 — unsellable at Rs 1,099"* and
rejected it.

Rs 1,099 is the point below which CPP headroom gets too thin. It says nothing
about a ceiling. A product that justifies a higher price should carry one.

## What the numbers actually say

C021, cordless 9-in-1 electric spin scrubber, DeoDap cost Rs 911
[source: deodap.in, 2026-10-12]. All figures [computed]:

| Selling price | RTO assumed | Blended contribution | Break-even CPP | Target CPP |
|---|---|---|---|---|
| Rs 1,099 | 30% | **-Rs 7** | n/a | n/a |
| Rs 1,799 | 45% | Rs 390 | Rs 331 | Rs 232 |
| Rs 2,499 | 45% | Rs 830 | **Rs 703** | **Rs 492** |

At Rs 1,099 the contribution really is negative, so the arithmetic in the
rejection was right. The reasoning was not: I never asked what the product
could carry. At Rs 2,499, and even after assuming a punishing 45% RTO, its
target CPP of Rs 492 is **the largest headroom on the shortlist** against a
real Indian CPP of Rs 200-250.

C021 is reinstated at rank 4.

## The same error, applied to everything else

Every other candidate was also priced at the floor by default. Repriced to
what each can carry, within the Rs 1,099-1,699 band:

| id | cost | was | now | target CPP | profit/order |
|---|---|---|---|---|---|
| C016 | Rs 159 | 1,099 | **1,299** | Rs 437 | Rs 221 |
| C019 | Rs 74 | 1,099 | **1,199** | Rs 432 | Rs 219 |
| C017 | Rs 96 | 1,099 | **1,199** | Rs 422 | Rs 213 |
| C003 | Rs 200 | 1,099 | **1,299** | Rs 418 | Rs 211 |
| C021 | Rs 911 | rejected | **2,499** | Rs 492 | Rs 249 |

C016 at Rs 1,299 rather than Rs 1,099 lifts target CPP from Rs 348 to Rs 437
and profit per order from Rs 176 to Rs 221 — a 26% improvement from changing
a number I had no reason to hold fixed.

## Why there is still a ceiling, just not the one I was using

Pricing up is not free, and these are the real limits:

1. **Conversion falls as price rises.** The model holds CPP constant across
   prices, which is wrong in the optimistic direction: a Rs 2,499 product has
   a genuinely higher CPP than a Rs 499 one. Headroom grows with price, but so
   does the CPP that has to fit inside it. The two partly cancel.
2. **COD refusal rises with price.** Refusing a parcel costs the buyer
   nothing, and Rs 2,499 in cash at the door is a real ask. The Rs 500-1,500
   band in `research/LEARNING-videos-2.md` exists for exactly this reason.
   The 45% RTO above is a guess in the right direction, not a measurement.
3. **Capital at risk per order.** At Rs 911 of stock per parcel, one refused
   C021 costs about six times a refused C016. Against a Rs 15,000 cap that
   changes how many shots we get.

## Rule going forward

**Price each product at what it can carry, inside Rs 1,099-1,699, and treat
anything above that band as an explicit exception with its own RTO
assumption.** Never default to the floor. The floor is a test a product must
pass, not the answer.
