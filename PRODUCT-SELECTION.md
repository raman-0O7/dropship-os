# Product Selection — Home Decor for Women / Homemakers

Shortlist 8–10 from DeoDap, score them, test the top 3. Score honestly;
the point is to kill bad candidates before they cost you ad money.

## Hard filters (fail any one → out, no scoring)

- **Breakable.** Glass, ceramic, mirrors, resin figurines. Courier handling
  in India plus an RTO leg means damage, refunds and angry reviews. This
  rules out a lot of attractive decor. Accept it.
- **Heavy or bulky.** Over ~700g or any dimension over ~35cm pushes
  shipping past Rs 100/leg and breaks the math.
- **Cheap single item with no bundle path.** If it cannot reach Rs 899
  as a set, skip it.
- **Available cheaper on Amazon/Flipkart/Meesho with 2-day delivery.**
  Our 5-7 day shipping cannot win that comparison. Check this early; it
  kills a lot of otherwise good candidates.
- **Sizing or fit involved.** Returns go vertical.
- **Anything with a warranty.** Narrowed 2026-10-12 from a blanket
  "no electrical" ban, which was a conservative default, not an
  evidence-based rule — and it was excluding two of our four strongest
  candidates (garment steamer, clip-on fan). The real risk is warranty
  claims, service expectations and safety liability, not electricity
  itself. So: **no mains-powered heating elements, no motors, nothing a
  customer would expect to claim a warranty on.**

  Refined again 2026-10-12 by the owner, and this is the final form:
  **battery or USB powered is allowed; anything that plugs into mains is
  not; and we give no warranty on anything.** A battery clip-on fan or a
  USB gadget passes. A garment steamer, iron, geyser or heater plugs into
  the wall and carries a warranty expectation, so it fails.

## Scorecard (1–5 each; test nothing under 20/30)

| Criterion | What a 5 looks like |
|---|---|
| **Margin headroom** | Target CPP from the calculator is Rs 350+ |
| **Visual stopping power** | Looks striking in a 3-second phone video; the transformation is obvious |
| **Problem it solves** | Hides clutter, saves space, makes a room look finished — not just "pretty" |
| **Durable in transit** | Fabric, plastic, wood, metal, silicone. Survives a drop |
| **Proven by a long-running ad** | A competitor has run ads on it for 6+ months |
| **Bundle / repeat path** | Natural set of 2–4, or a reason to reorder |

## Where this niche actually wins

Home decor buyers scroll Instagram and Facebook Reels. The product has to
*show* a before-and-after. Categories that film well, ship well and bundle
naturally:

- Wall organisers and floating shelves (metal or engineered wood)
- Fabric storage baskets and under-bed organisers
- Kitchen drawer and spice organisers — sets of 4–6 hit Rs 899 easily
- Curtain and door accessories, macrame hangings
- Artificial plants and planters (plastic, not ceramic)
- Fridge and cabinet liners, sets

Avoid: idols and religious decor (sentiment risk on damage), candles and
diffusers (leakage), anything described as "antique finish" (quality
variance).

## Creative angle, decided per product before testing

Write one sentence: *the frame at second 1, and the frame at second 5.*
If you cannot describe a visible change between those two frames, the
product will not carry a Reel, and this niche lives on Reels. Go back to
the shortlist.

## Checking competition — corrected

**Earlier versions of this file had this backwards.** It said few or no
competitors was the good sign. Published methodology says the opposite,
and the reasoning is sound: an ad running six months or longer is very
likely profitable, because nobody funds a loser for six months
[source: Koala Apps]. A long-running competitor is the strongest free
*validation* you can get.

Meta Ad Library (free, no login, India filter):

| What you see | Read it as |
|---|---|
| Ads 6+ months old | **Proven demand. Good sign.** |
| Every ad under 4 weeks old | Unproven. Wait and watch |
| Many advertisers, all the same creative angle | The angle is used up — change the angle, not the product |
| Competitors cheaper with faster delivery | Reject |

An empty Ad Library result is not a free run at a virgin market. Usually
it means nobody has made this product work. Full method in
`RESEARCH-METHOD.md`.

---

## Shortlist gates (added 2026-10-12)

The 13-KPI scorecard decides what enters the Candidates log. These three
gates decide what reaches the Shortlist. Reasoning and evidence:
`research/FINDING-price-anchor-vs-ad-proof.md`.

Run them in this order — cheapest and most absolute first.

### Gate 1 — supply exists

In the DeoDap catalogue, in stock, with cost and weight recorded.

```
.venv/bin/python tools/deodap_lookup.py "<product>" --limit 3
```

Try at least three phrasings before concluding it is absent. No supply means
no product, whatever the KPI score: this removed C001, which was top of the
shortlist at 11/13.

Record `deodap_cost`, `deodap_weight_g`, `deodap_rating`, `deodap_reviews`,
`deodap_in_stock`, `deodap_url`. Cost and weight are the inputs to
`unit_economics.py`, so this gate is also what makes the economics real
rather than estimated.

DeoDap is a **single supplier, not a marketplace**. There are no competing
sellers to rank, no public per-seller inventory and no order counts. The
product rating is the available quality signal. Prefer >= 4.4 with >= 100
reviews; a low rating is a return-rate and RTO risk.

### Gate 2 — advertiser proof

**>= 3 distinct advertisers, and at least one running >= 6 months.**

Count advertisers, never ads. One advertiser routinely runs 10+ ads off a
single creative, so an ad count overstates competition roughly tenfold.
Exclude national brands, marketplace affiliates (Meesho, Flipkart, Wishlink)
and advertisers whose copy is not aimed at India.

Store up to three Ad Library permalinks per product
(`https://www.facebook.com/ads/library/?id=<Library ID>`) — they are the raw
material for our own creatives later.

### Gate 3 — price anchor (the one that bites)

**Record what competitors actually charge.** If the identical item is being
advertised below our price floor, set `ad_price_anchor_risk = HIGH` and treat
it as blocking.

A long-running competitor ad proves the product sells *and* fixes the price
it sells at. For an undifferentiated commodity the second fact can destroy
the first — C018 has thirteen months of proof and is unsellable at our floor
because eight advertisers have anchored it at Rs 399.

A HIGH anchor is only cleared by genuine differentiation: a bundle that is
not sold as a bundle elsewhere, personalisation, or a buyer segment the
incumbents are not reaching. "Better creative" is not differentiation.

**Consequence worth internalising:** the ideal product has demand proven by
several advertisers but has **not** yet been commoditised on price. That is a
narrower window than "lots of ads = good", and it is where to hunt.

### Gate 4 — perceived value (added 2026-10-12, REVISED same day)

**First revision was wrong.** It used a Meesho median as a hard price cap,
which contradicts the standing decision that marketplace price *taxes
conversion rather than capping price*, and it picked the cheapest platform in
India as the reference. Corrected below.

**The distinction that matters: who is anchoring, and does our buyer see it?**

- **Competitor ADS anchor hard.** They run in the same feed we advertise in.
  A buyer scrolling Reels sees a competitor's Rs 399 offer for the identical
  item minutes before or after ours. That is a real, blocking comparison.
- **Marketplace listings mostly do not.** Our buyer is not searching Meesho;
  they are impulse-buying from a video. A Meesho listing is a conversion tax,
  not a ceiling. Paying more than Meesho is the entire dropshipping model.

So the gate has one hard block, one judgement call, and one soft signal.

**HARD BLOCK — we cannot win on supply.** Marketplace retail price at or
below our DeoDap cost. Not a positioning problem, an arithmetic one: C021
retails on Meesho around Rs 924 against our Rs 911 cost.

**HARD BLOCK — recognisable commodity with a known price.** Items the buyer
has already owned, where a price is fixed in their head before the video
starts: a plastic masala box, a storage basket, a set of jars. No creative
argues someone out of a price they already know. The test is whether a
typical buyer could guess the price within about 30%, not what any one
platform charges.

**SOFT SIGNAL — marketplace multiple.** Record the median and range, and
treat a large multiple as a drag on conversion to be priced into
expectations. Do not block on it. Use the broadest-market reference available
(Amazon or Flipkart before Meesho, which sits at the bargain end).

Record `market_median`, `market_range`, `market_multiple` as information.
Block only on the two hard conditions above.

Reasoning and measurements: `research/FINDING-perceived-value-gate.md`.
