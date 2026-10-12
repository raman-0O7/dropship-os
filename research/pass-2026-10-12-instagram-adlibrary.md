# Research pass — 12 Oct 2026, Instagram + Ad Library

Second pass after the owner refined the hardware rule (battery/USB allowed,
mains not, no warranty on anything) and supplied the 13-KPI filter.

## What was done

- **Instagram**: mined `#kitchengadgets`, `#homefindsindia`, `#kitchenhacks`
  — 65 posts captured with like counts and captions, 44 of them with an
  identifiable product.
- **Feed warming**: 6 product posts liked on the research account, chosen
  deliberately rather than from the generic Reels feed. The untrained feed
  was serving kirtan videos; liking those would have taught it the wrong
  thing. Liking the specific product posts teaches it precisely.
- **Ad Library**: `chopper` query, India, active video ads.
- Candidates log grew from 15 to **22 products**, 10 of them live.

## Best finds

| Score | Product | Evidence |
|---|---|---|
| **12/13** | Electric garlic peeler (battery) | **3M likes** — highest engagement of anything found |
| 11/13 | Silicone stretch fresh-keeping lids | 95K likes |
| **11/13** | **Manual vegetable chopper** | 49K likes **+ a 12-month India ad** |
| 11/13 | 13-in-1 multi chopper | Meesho-affiliate ad, strong hook |
| 10/13 | Masala box / spice organiser | 32K likes |
| 10/13 | Electric spinner scrubber (battery) | 35K likes |

### The standout is the manual vegetable chopper

**It is the only candidate with both signals**: viral on Instagram *and* a
dropshipper ad that has run in India for 12 months ("Home And Kitchen SW 3",
CHOP10 Vegetable Chopper, running since 7 Oct 2025). Everything else has one
or the other.

It is also manual — no battery, no motor, no warranty, nothing to fail.

Note Wonderchef and Borosil advertise in the same space. The dropshipper is
surviving next to two real brands, which is a good sign rather than a bad
one: the category supports multiple advertisers.

### The one that scores highest is the one to be careful about

The electric garlic peeler scores 12/13 on 3M likes. It passes the refined
rule because it is battery powered. But it has a **motor**, and a motorised
gadget that fails generates replacement demands whether or not we offer a
warranty. Logged as a candidate with the risk flagged — owner's call.

### Silicone lids pass a KPI almost nothing else does

**#9, saves people money.** They replace cling film, which is a recurring
purchase. Most products fail this KPI; a genuine pass is worth noting.

## Method notes worth keeping

- **Instagram hashtag grids carry no captions.** Collect post links from the
  grid, then read each post's `og:description`, which contains like count,
  author, date and caption. Scales to dozens per pass.
- **Roughly a third of captions are unusable** — "comment for link" and
  nothing else, because driving comments is the whole business model. Those
  posts cannot be identified without watching the video.
- **Ad Library's India filter leaks.** The URL keeps reasserting
  `is_targeted_country=false`, so results include ads merely *visible* in
  India. Check the advertiser before trusting a result.
- The `cash on delivery` query remains the best way to isolate Indian
  dropshippers from brands and affiliate influencers.

## Still blocking real economics

Every score above is judgement, not measurement. **No candidate has a
supplier cost or weight**, so no unit economics exist for any of them.
DeoDap access is the gate.
