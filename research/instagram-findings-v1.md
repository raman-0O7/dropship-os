# Instagram findings — what is actually going viral (India)

**Date:** 2026-10-12 · **Method:** dummy Instagram account, hashtag mining,
captions and like-counts read from the DOM. Thumbnails did not render (ad
blocker), and **I cannot watch video** — so this is caption + engagement
evidence only, not an assessment of the creative.

## How it was done

Hashtag grids give no captions, so: collect post links from the grid, then
read each post's `og:description`, which carries like count, author, date
and caption. Fast, and scales to dozens of posts per pass.

Tags used: `#amazonfindsindia` (India), `#amazonfinds` (global, useful as
the Europe/US-to-India leading indicator per `RESEARCH-METHOD.md` §2b).

## What is viral right now — India tag

| Likes | Product |
|---|---|
| **257K** | **Portable handheld garment steamer** — "Wrinkles? Not anymore... quick, handy & travel-friendly" |
| 222K | Sink-related gadget (product not named in caption) |
| **199K** | **Detachable / removable cookware handle** — "An essential removable handle for your cookware" |
| 138K | Unnamed ("comment for link") |
| 50K | Unnamed |
| 33K | Unnamed home finds |
| **23K** | **360-rotating multi-purpose storage rack** |
| 15K | Portable printer |

## Global tag — leading indicators

| Likes | Product |
|---|---|
| 228K | Clip-on stroller/pram fan (toddler) |
| 150K | Bedroom finds compilation |
| 93K | **Handheld clothes steam iron** — same product as the 257K India post |
| 31K | Kitchen product (22K comments — unusually high comment ratio) |

**The garment steamer appears in both the India and global tags.** That
cross-signal is the strongest single finding of this pass.

## Candidate assessment against our filters

| Product | Light | Non-fragile | Bundles | Non-branded | Verdict |
|---|---|---|---|---|---|
| **Detachable cookware handle** | yes | yes | yes, set of 2-3 | yes | **best fit** |
| Portable garment steamer | yes | yes | no | yes | **electrical — currently excluded** |
| 360 rotating storage rack | yes | yes | maybe | yes | viable, lower engagement |
| Clip-on fan | yes | yes | no | yes | electrical |
| Portable printer | yes | no | no | mostly branded | reject |

### Top pick: detachable cookware handle

Tiny, light, unbreakable, cheap, naturally sold as a set, and it solves a
stateable problem (pans nest for storage; pan goes oven-to-table). Kitchen
is on the practitioner's **low-RTO category list**. 199K likes says it
stops a thumb.

### The problem this pass exposes: our electrical exclusion

**Two of the four strongest candidates are electrical** (garment steamer,
clip-on fan), and `PRODUCT-SELECTION.md` rejects electrical outright on
warranty, safety and RTO grounds.

That rule may be costing us the best products. Handheld steamers are a
proven, heavily-advertised dropship category worldwide. The exclusion was
written as a conservative default, not from evidence.

**Recommend revisiting it** — possibly narrowing to "no mains-powered
heating elements, no products needing a warranty claim", which would still
exclude geysers and heaters but allow a USB fan or a low-wattage steamer.
Owner's call; it materially widens the candidate pool.

## Honest limits of this pass

- **Captions are deliberately vague.** Most say "comment for link" and
  never name the product, because the whole business model is driving
  comments. Several high-engagement posts are therefore unidentifiable
  without watching the video, which I cannot do.
- **These are Amazon affiliate reels, not dropship ads.** High engagement
  proves the product has visual appeal and demand — it does not prove
  anyone is profitably dropshipping it. It also means the product *is on
  Amazon*, so the undercut check in Stage 3 still applies to every one.
- **Likes are on the reel, not the product.** A great creator can make a
  dull product go viral.
- The feed has not been trained yet. Hashtag mining is a one-off pull;
  the method's compounding value comes from liking and watching so the
  algorithm serves products continuously. Not done — that is an action on
  the owner's account and needs his go-ahead.

## Next

1. Owner decides on the electrical exclusion.
2. Marketplace undercut check on the cookware handle and the storage rack.
3. DeoDap search for both → supplier cost and weight → **first real unit
   economics of this project**.
