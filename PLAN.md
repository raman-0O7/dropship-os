# Home Decor Dropshipping — Capped Experiment

**Niche:** home decor + home accessories, targeting women / homemakers in India
**Supplier:** DeoDap
**Hard cap:** Rs 15,000 total. **Hard stop:** 90 days from first ad rupee.
**Started:** 2026-10-11

This is a paid learning experiment with a kill switch, not a business plan.
If the cap is hit, it ends. That rule is the whole point.

---

## 1. Budget allocation (Rs 12,000 working, Rs 3,000 reserve)

| Item | Budget | Notes |
|---|---|---|
| DeoDap subscription | 1,500–2,500 | verify current plan price on their site |
| Domain (.in or .com) | 700–1,200 | one year |
| Shopify | 1,000–2,400 | check the Rs 20/month intro offer; if unavailable, Basic is ~1,800/mo |
| Creatives, logo, copy | 0 | AI + your own phone camera |
| **Ad testing** | **7,000** | the only line that buys information |
| Reserve (refunds, RTO losses) | 3,000 | do not spend this on ads |

Ads are ~58% of the working budget. If the fixed costs creep above
Rs 5,000, cut a product from the test list rather than cutting ad budget —
underfunded tests produce noise, not answers.

## 2. Price point — decided by the math, not by taste

Run `tools/unit_economics.py` before committing to any product. At the
default India assumptions (RTO 30%, prepaid 20%, Rs 70 shipping each way):

| Selling price | COGS | Break-even CPP | Target CPP (30% margin) |
|---|---|---|---|
| Rs 599 | 180 | 196 | 137 |
| Rs 899 | 280 | 342 | 239 |
| Rs 1,299 | 400 | 546 | 382 |
| Rs 1,799 | 550 | 802 | 561 |

Meta CPP for home decor impulse buys in India commonly lands in the
Rs 150–400 range. At Rs 599 you are betting on the good end of that range
and one bad week wipes you out. **Target Rs 899–1,499**, reached with
bundles or sets if single items are cheap. This single decision matters
more than anything in the ad account.

## 2b. COD checkout policy — decided, with a phase gate

Two levers, and they are not the same kind of thing. A prepaid discount is
a carrot with no friction. A partial-COD advance (customer pays Rs 99
online, rest on delivery) adds real checkout friction and will cost some
orders. Run `tools/cod_policy.py` to see the trade for a given product.

For the Rs 599 product, ad spend held fixed:

| Policy | Blended per order | Order volume it can afford to lose |
|---|---|---|
| Plain COD | Rs 196 | — (baseline) |
| Prepaid 5% discount only | Rs 209 | 6% |
| **Partial COD only** | **Rs 279** | **30%** |
| Both together | Rs 276 | 29% |

That last column is the whole decision. Partial COD has to destroy more
than 30% of your orders before it is worse than doing nothing — and it
holds up under pessimism: even if the advance only pulls RTO from 30% to
25%, the cushion is still 16%. Real friction cost is very unlikely to
exceed that. **Partial COD is the right long-run setting.**

Note that Both is slightly *worse* than partial COD alone: the discount
cannibalises partial-COD orders, which are already nearly as valuable, at
full price. Do not stack them without checking.

### But not during product testing

Turn partial COD on only after a product proves it sells. During the
Rs 2,000-per-product tests:
- You need maximum order count, because order count *is* the signal.
- At ~17 orders per product you cannot detect a 20% conversion difference.
  There is no sample size here for an A/B test; do not pretend otherwise.
- Checkout friction confounds the question you are actually asking, which
  is "does anyone want this product".

So: **phase 1 = plain COD + prepaid discount at checkout. Phase 2
(scaling a winner) = switch to partial COD** and watch the order rate.

If you keep the Rs 99 when a customer refuses the parcel, say so in plain
language at checkout and in the confirmation message. Silently keeping it
produces chargebacks, payment-gateway complaints and the kind of reviews
that end a store.

## 2c. Launch timing — decided from ad-cost seasonality

Diwali 2026 is ~8 November [source: HinduTone, conflicting sources —
confirm]. Peak home-decor buying is happening right now and runs to then.
It is tempting. Do not chase it.

Festive CPMs run 30-60% above baseline [source: Criteo, paceads]. On a
Rs 899 product with break-even CPP Rs 342:

| Period | CPP | Verdict |
|---|---|---|
| Baseline months | Rs 300 | breaks even |
| Festive peak (+40% CPM) | Rs 420 | **loses money** |
| January trough (-15% CPM) | Rs 255 | breaks even |

The same product loses money in late October and works in January. With
Rs 7,000 of ad budget we cannot outbid brands during peak season, and
every test would cost ~40% more for identical learning.

**Decision: build through Oct-Nov, start testing in January.** The 90-day
clock starts at the first ad rupee, so building costs us nothing in time.
The payoff is a tested, automated machine ready for Valentine's and Holi,
and for Diwali 2027 at full strength rather than half-built.

Revisit only if a candidate shows a long-running proven ad AND a target
CPP above Rs 450, which would absorb festive inflation.

## 2d. GST — we start unregistered

**Corrected.** Earlier versions of this section argued the owner was
already GST-registered and therefore had to charge GST. That was wrong.
The GSTIN he has access to is **registered on his mother's PAN**, which
makes it a different taxable person with no bearing on this business. He
is also closing it.

The business runs under **his own PAN, which holds no GST registration.**
So:

- **Start unregistered.** Own-website sales follow the normal threshold,
  Rs 40 lakh for goods. Section 24's "from the first sale" rule applies to
  selling *through* a marketplace, not from our own store
  [source: qikink, disytax].
- **Do not use the mother's GSTIN for this business.** It would make her
  PAN the seller of record and put her name on the tax liability and the
  business. Keep the two entirely separate.
- **Closing her GSTIN is her decision, not ours.** It is independent of
  this plan now. Decide it on whether her business needs it.

### What being unregistered actually costs

| Item | Cost |
|---|---|
| 18% GST on Meta ad spend, not reclaimable | ~Rs 1,260 on Rs 7,000 of ads |
| DeoDap B2B invoicing may prefer a GSTIN | check; many suppliers sell to unregistered buyers |
| Meta Business verification for WhatsApp | use Udyam instead — see `AUTOMATION.md` |

The ad GST is already baked into every number the tools print: with
`--gst 0` they divide affordable CPP by 1.18, because Meta's 18% is a real
surcharge we cannot reclaim.

### Two rules while unregistered

1. **Track turnover against Rs 40 lakh** and register before crossing it.
   Not a near-term risk at this scale, but it is a hard line.
2. **Do not list on Amazon, Flipkart or Meesho.** Selling through a
   marketplace triggers mandatory GST registration from the first sale.
   Own website only until we choose to register.

Not tax advice; sources are secondary. Confirm with a CA.

## 3. Kill criteria — written down before any money moves

Per product:
- **Kill at 2.5x break-even CPP in spend with zero orders.** For a Rs 899
  product that is Rs 855. No debating it at the time.
- **Kill if actual CPP stays above break-even after 10 orders.** Ten orders
  is enough signal; waiting for 30 is how budgets die.
- **Kill if RTO on that product exceeds 40%** even when CPP looks fine.
  Delivered margin is the only margin.

Overall:
- Stop at Rs 15,000 total spend, whatever the state of things.
- Stop at day 90.
- **Scale only** a product that is profitable after ad cost, RTO and
  shipping — not one that is profitable on revenue.

## 4. Sequence

**Week 1 — foundation (no ad spend)**
1. DeoDap account, confirm subscription cost and whether they push orders
   to Shopify automatically.
2. Shortlist 8–10 products with `PRODUCT-SELECTION.md`, narrow to 3.
3. Run each through `tools/unit_economics.py`. Anything that cannot clear
   a Rs 250 target CPP is out.
4. Build the store. One niche, coherent look, real trust signals.

**Week 2 — automation before ads**
5. Order webhook + COD confirmation flow (`AUTOMATION.md`). This is live
   *before* the first order arrives, because the first RTO teaches you
   nothing you cannot already predict.
6. Ad reporting pull, so kill decisions are mechanical.

**Weeks 3–6 — test**
7. Three products, Rs 2,000 each, sequential not parallel. Sequential
   keeps attention on one set of creatives and makes the signal readable.
8. Apply the kill rules on schedule, not on feeling.

**Weeks 7–12 — scale or stop**
9. One winner: reinvest its own profit, do not add outside money.
10. No winner: stop. Write down what the Rs 12,000 bought you.

## 5. What would make this worth continuing past day 90

A product with CPP under target for two consecutive weeks at Rs 500+/day,
RTO under 25% after the confirmation flow, and under 4 hours a week of
your time. If all three are not true, the honest answer is that your hours
are worth more somewhere else.
