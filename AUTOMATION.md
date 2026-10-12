# Automation Build Plan

Order of work is deliberate: the COD confirmation flow earns more than
everything else combined, so it ships first. Nothing here needs to be
elegant; it needs to be running before the first order.

## Priority 0 — COD verification: BUY, do not build

**This section previously said to build a WhatsApp confirmation service.
That was wrong and would have wasted weeks.** Purpose-built Shopify apps
already do this, India-first, for roughly Rs 1 per message. Being a
developer is a reason to spend the build time on something that is not a
solved problem.

### Better still: OTP at checkout, not confirmation after the order

The original design confirmed orders *after* they were placed. Verifying
the phone number *at checkout* is strictly better: a fake or mistyped
number never becomes an order at all, which is the single largest RTO
cause. No messaging infrastructure, no Meta Business verification, no
WhatsApp API.

### Options found (verify current pricing on each listing)

| App | What it does | Reported price |
|---|---|---|
| [COD Guard](https://apps.shopify.com/codguard-1) | SMS OTP on COD orders, partial payments | free install, ~Rs 1/message |
| [COD King](https://apps.shopify.com/cash-on-delivery-cod-order-confirmation) | OTP **plus partial/deposit COD** | free to install |
| [Cartsaver OTP CoD](https://apps.shopify.com/xtnd-order-confirmation-otp) | OTP via WhatsApp, SMS or email | has a free plan |
| [Hillteck](https://apps.shopify.com/cod-order-verification) | IVR call + WhatsApp confirmation, most India reviews | unclear; usage-based |
| [Cashify COD Confirmation](https://apps.shopify.com/cod-order-confirmation) | IVR confirmation calls | ~$0.025/call, ~$0.015/OTP |

**COD King is the closest fit**, because it does OTP *and* partial COD —
the two exact levers modelled in `PLAN.md` §2b — in one app. Shortlist
COD Guard as the cheaper OTP-only fallback.

The app is also the messaging provider, so DLT/SMS registration and
WhatsApp verification become their problem, not ours. That is most of the
reason to buy rather than build.

### Phase it, per `PLAN.md` §2b

- **Phase 1 (testing):** OTP verification on at checkout. Partial COD OFF.
  OTP costs almost no conversion — it blocks fake numbers, not real buyers.
- **Phase 2 (scaling a winner):** turn partial COD on, watch the order
  rate against the 30% cushion.

### What we still build ourselves

Not the confirmation flow. These:

1. **Targeted prepaid offer.** Worth ~Rs 129 per converted order, the
   single biggest lever in `PLAN.md` §2b. Offered to COD buyers only,
   after they order, so we do not discount people who would have paid
   anyway. Check whether the chosen app can do this; if not, it is ours.
2. **Outcome logging.** Delivery rate split by verification outcome
   (verified / unverified / cancelled). This is what tells us whether to
   start cancelling non-responders, and no app will give it to us in the
   shape our economics model needs.
3. **The decision layer.** Per-product CPP vs break-even, printing
   scale / watch / kill. See Priority 2.

### WhatsApp order updates — not blocked after all

Earlier versions of this file treated Meta Business verification as a
blocker needing a GST certificate. It is not.

- **Verification is not required to go live.** An unverified WhatsApp
  Business account handles **up to 250 conversations per 24 hours**
  [source: go4whatsup]. At test-phase volume of a few orders a day that is
  ample; verification only raises the cap.
- **GST is not the only verification document.** Udyam (MSME) registration
  is the commonly named alternative for Indian sole proprietors
  [source: richautomate, intigate]. One source claims GST is mandatory —
  treat that as the stricter, unconfirmed reading, and check the accepted
  list in Meta Business Manager's Security Center before applying.
- Legal name and address must match exactly across documents. A trade name
  will not match.

**So: start WhatsApp unverified now, and do the free Udyam registration as
insurance for when the cap matters.**

Order updates are worth having beyond support load: a customer who knows a
parcel is arriving is measurably less likely to refuse it, so proactive
tracking messages are an RTO lever, not just a courtesy.

### Checkout partners already cover some of this

The plan is Razorpay Magic Checkout or Shiprocket for OTP-based checkout.
Both bring more than OTP, which reduces what we build:

| Partner | Relevant capability | Caveat |
|---|---|---|
| [Razorpay Magic Checkout](https://razorpay.com/docs/payments/magic-checkout/features) | COD RTO intelligence scoring address, pincode, IP and customer history; **converts COD to prepaid post-order with a discount, link sent over WhatsApp**; RTO analytics | On-demand — must request activation. No public pricing. OTP verification not documented |
| [Shiprocket Engage](https://apps.shopify.com/shiprocket-engage) | Order confirmation, address verification, COD-to-prepaid, WhatsApp tracking updates | ~Rs 2.49/order claimed, listing inconsistent on currency. 3.0 rating from 6 reviews, support complaints |

**Magic Checkout's post-order COD-to-prepaid conversion is exactly the
Rs 129/order lever from `PLAN.md` §2b.** If it works as documented we do
not build that either — confirm on activation, since the feature is gated
and unpriced.

Razorpay's RTO risk scoring is the more interesting part: it decides
*which* COD orders to accept at all, which sits upstream of everything we
modelled. Ask about it when requesting activation.

### Caution: our RTO assumptions may be optimistic

A practitioner with a claimed ₹90cr track record reports that calling every
customer, cancelling fake addresses and sending WhatsApp updates moves RTO
from about **50% to about 40% — roughly 10 percentage points**
[source: `research/LEARNING-from-practitioner-video.md`].

Our model assumes better: confirmed orders at 15% RTO against a 30%
baseline. Partial COD is structurally different — money paid upfront is
commitment, not just a confirmation — so a larger drop there is defensible.
But **treat the confirmation-only figures as optimistic** until we have our
own order data, and re-run the policy comparison at a 10-point improvement
before relying on it.

### Do not auto-cancel non-responders on day one

Modelled on 100 COD orders of a Rs 899 product:

| Policy | Delivered | RTO | Contribution |
|---|---|---|---|
| No verification | 70 | 30 | Rs 16,620 |
| Cancel only explicit "no" | 70 | 20 | **Rs 18,290** |
| Also cancel all non-responders | 51 | 9 | Rs 14,256 |

The third row has the *best* RTO rate and the *worst* profit. Plenty of
people ignore a message and still accept the parcel; cancelling them
destroys more margin than the RTO it avoids. Low RTO is not the goal —
contribution is. RTO rate is a vanity metric you can always improve by
refusing to sell anything.

Checkout OTP is the exception and the reason it is better: it blocks
numbers that were never real, without touching a genuine buyer.

## Priority 1 — Order pipeline

- Shopify webhook → queue → supplier order placement.
- First check whether DeoDap's Shopify app already pushes orders. If it
  does, do not rebuild it.
- Tracking sync back to Shopify, and a proactive shipping update to the
  customer. Cuts "where is my order" messages, which are most of support.

## Priority 2 — Ad reporting and kill enforcement

Daily pull from the Meta Marketing API into a table with, per product:
spend, purchases, actual CPP, break-even CPP from the calculator, and
delivered-order contribution after RTO.

The report's job is to print one of three words per product: **scale**,
**watch**, **kill** — against the thresholds already written in `PLAN.md`.
Decisions made in advance and enforced by a script are the only ones that
survive contact with a losing campaign.

## Priority 3 — Content and support assistance

- AI-drafted product copy, SEO, ad variations. You approve everything.
- Draft replies to customer messages. You send them.

## Guardrails — not negotiable

- **No AI with spending authority.** Daily caps set at the Meta platform
  level, not in your code. One runaway campaign is a large share of a
  Rs 15,000 budget.
- **No unsupervised customer messaging** beyond the fixed COD
  confirmation template.
- **Every automated action logged** with enough detail to reconstruct what
  happened. When numbers look wrong, you need to know whether the problem
  is the product or the pipeline.
