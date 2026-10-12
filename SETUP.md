# Setup — what Claude needs for the research pipeline

Status 2026-10-12. Reordered after research: **demand signals first, the
supplier catalog last.** See `RESEARCH-METHOD.md` for why.

## Tier 1 — Needed to start research this week

| # | Item | Cost | Unlocks |
|---|---|---|---|
| 1 | **Chrome extension permissions** for the sites below | free | Everything in Stage 1-3. Meta Ad Library has no public API for commercial ads, so this is browser work or nothing |
| 2 | **Google Drive connector** (connect in Claude) | free | Shortlists land in a Sheet you and your partner score in |

Sites to allow the Chrome extension on:

- `facebook.com/ads/library` — ad age, the one signal that proves a product sells
- `trends.google.com` — India demand curves, 90-day and 5-year
- `amazon.in` — Best Sellers and Movers & Shakers (hourly, 24h window)
- `flipkart.com`, `meesho.com` — tier-2/3 demand, closest to our buyer
- `trends.pinterest.com` — home decor is Pinterest-native and under-used here
- `instagram.com` — Reels formats and hooks

That is the whole research stack and it costs nothing.

## Tier 2 — Once candidates exist (not before)

| # | Item | Cost | Unlocks |
|---|---|---|---|
| 3 | DeoDap catalog export (CSV: name, cost, weight, stock, URL) | incl. | Sourcing products research has already validated |
| 3b | ~~Evaluate Roposo Clout~~ | — | **Dropped. Roposo Clout shut down 1 Apr 2026.** The same practitioner now names **DeoDap** as his pick, unsponsored — which validates our existing choice. See `research/LEARNING-videos-2.md` |
| 4 | Koala Inspector (free Chrome extension) | free | Competitor Shopify catalogs and best-sellers |

## Tier 3 — Before the first campaign (January, per `PLAN.md` §2c)

| # | Item | Unlocks |
|---|---|---|
| 5 | Shopify store + Admin API token | Order webhooks, COD confirmation flow |
| 6 | Meta Marketing API, read-only | Daily per-product CPP vs break-even; scale/watch/kill |
| 7 | Razorpay account | Prepaid payments. **No GSTIN required** — see below |

## Deliberately NOT buying

**Paid spy tools.** Minea, Dropship.io, Sell The Trend, PiPiAds run
$39-49/month (Rs 3,300-4,200). One month of one tool is a third of the
entire budget, and they mostly index Western ads. The free stack plus
manual browser work covers the same ground.

**Ad account spending permission.** I never place, raise or resume a
campaign. Read-only metrics is enough.

## GST — starting unregistered

The GSTIN the owner has access to is on **his mother's PAN** — a separate
taxable person, irrelevant to this business, and being closed. The
business runs on his own PAN, which has no registration.

- **No GSTIN needed** for Razorpay, for our own website, or to operate.
- **Do not use the mother's GSTIN here.** It would put her PAN on the tax
  liability and make her the seller of record.
- **Rs 40 lakh threshold** applies; track turnover against it.
- **Never list on Amazon/Flipkart/Meesho while unregistered** — selling
  through a marketplace makes GST mandatory from the first sale.
- Unregistered means the 18% GST on Meta ads is absorbed, ~Rs 1,260 on
  Rs 7,000 of ads. Already priced into every tool output.

## Udyam registration — do it (reason changed)

Free MSME registration on udyamregistration.gov.in, needs only Aadhaar and
PAN, auto-verified against the PAN and GST databases, no documents to
upload [source: cleartax, kanakkupillai].

It gives priority-sector lending, collateral-free loan eligibility,
government scheme access and tender preference, plus protection against
late payment from buyers.

**Do it.** It is the named non-GST route through Meta Business
verification for the WhatsApp API [source: richautomate, intigate], which
matters if the GSTIN is ever cancelled or the business moves to another
entity. Free, Aadhaar-only, and removes a future blocker. Not urgent —
WhatsApp works unverified up to 250 conversations/day — but there is no
reason to skip something free that closes a risk.

Not tax advice; sources are secondary blogs. Confirm with a CA.

## Honest note on "working day and night"

I do not run continuously. I run when a session starts or when something
schedules me. Real mechanisms: **`/schedule`** for cron-driven runs (a
weekly trend scan is genuinely useful now; a daily campaign report is not,
until there are campaigns) and **`/loop`** within a session.
