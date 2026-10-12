# Ad Library findings — who is actually winning in India right now

**Date:** 2026-10-12 · **Source:** facebook.com/ads/library, India, active
ads, video only, read directly in browser.

## The search trick that worked

Searching a category term ("organizer") returns mostly Meesho and Flipkart
**affiliate influencers**, not dropshippers. Searching **"cash on
delivery"** isolates real Indian D2C and dropship stores, because almost
every one of them puts that phrase in the ad copy and brands do not.

Use that as the standard query going forward. >50,000 results.

## Long-running ads = proven profitable

`RESEARCH-METHOD.md` §2: an ad running 6+ months is very likely profitable.
Everything below is an **active** ad, with its real start date.

| Advertiser | Product | Running since | Age |
|---|---|---|---|
| **Glamorizee** (glamorizee.com) | Personalised name necklace / bracelet, Rs 199 | **20 Mar 2025** | **19 months** |
| Curiospot (curiospot.com) | Combo of 5 checked shirts, Rs 999 | 25 May 2025 | 17 months |
| Wowgifts (wowgifts.co.in) | 6-in-1 gift combo, 50% off | 2 Oct 2025 | 12 months |
| Param Innovative | Kids Intelligence E-book, ages 2-7 | 25 Nov 2025 | 11 months |
| Heaven Magic Beauty | Bridal brightening cream | 9 Jan 2026 | 9 months |
| Health & Wellness | Ear sound amplifier, Rs 599 | 5 Feb 2026 | 8 months |
| Toykoo (toykoo.in) | Maybach 1:24 diecast model | 23 Feb 2026 | 8 months |
| Perfectefyy (carefy.in) | Pack of 3 lycra pants | 6 Aug 2026 | 2 months |

**Glamorizee is the standout.** Nineteen months on the same product, with
many creative variants (King Name, Lion Name, Couple 2-Name, Silver
Bracelet) and a claim of "5 Lakh+ customers". Nobody funds 19 months of
Meta ads on a loser.

## Four patterns worth copying

**1. Personalisation defeats price comparison.** This is the big one. You
cannot search Amazon for a necklace with *your name on it* and find it
cheaper — it does not exist until it is made. Glamorizee has run 19 months
on exactly that. It structurally solves the problem in
`research/FINDING-niche-fails-undercut.md`: a visible cheaper alternative
taxes conversion, and personalisation removes the alternative.

**2. Combos priced at ~Rs 999.** Curiospot sells 5 shirts for Rs 999;
Wowgifts sells a 6-in-1 combo. Same bundling-to-a-price-point strategy
`tools/score_products.py` already implements. Independent confirmation that
bundling to clear a price floor is standard practice, not a workaround.

**3. Prepaid incentives are standard.** Toykoo offers **Rs 200 off on
prepaid orders**, in the ad copy itself. That is `PLAN.md` §2b in the wild,
and at a far more aggressive discount than the 5% we modelled.

**4. Gifting is a recurring angle.** Wowgifts, Glamorizee and Toykoo are
all gift-framed. Gifts justify a price premium and are not price-shopped
the way a utility purchase is.

## The awkward finding for our current niche

**Home organisers are not where Indian dropshippers are winning.** The
"organizer" search surfaced Meesho/Flipkart affiliate influencers and
short-lived ads, not long-running D2C stores. The long-runners are in
personalised jewellery, apparel combos, gift combos, beauty, education and
novelty collectibles.

Combined with the marketplace price data in
`FINDING-niche-fails-undercut.md`, the picture is consistent: home
organisation is marketplace territory, won on price and 2-day delivery.

## Recommendation

**Keep the buyer, change the product type.** Women 25-45 in India stays.
Move from commodity home organisation to **personalised / giftable items
for that buyer**, because it removes price comparison entirely rather than
asking the creative to overcome it.

The runner-up is **bundled home items at Rs 999-1,299** in the Curiospot
style — still viable, but it fights the marketplace gap head-on rather
than sidestepping it.

## Honest status

These are **validated competitors, not validated products for us.** Still
missing before any of this is a shortlist:

- Supplier cost and weight from DeoDap for each candidate → **no unit
  economics exist yet for any of them**.
- Whether DeoDap can even source personalised items. Personalisation
  usually needs a print-on-demand or custom supplier, not a stock
  dropshipper. **This may be the blocker on the top recommendation.**
- Visual hook written per product (Stage 2).
- Marketplace undercut check per product (Stage 3).
