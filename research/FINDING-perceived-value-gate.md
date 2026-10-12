# Markup ratio is the wrong question. "Is our price inside the range the
# buyer already sees?" is the right one.

Date: 2026-10-12. Prompted by the owner: *"a product costing us 74 isn't it
too much high cost to sell it at 1199??"* The instinct was right and it
removed three of six shortlisted products.

## Why markup ratio is not the test

The buyer does not know our cost. Rs 74 -> Rs 1,199 is 16x, and the multiple
by itself proves nothing: Indian dropshipping runs on exactly these ratios,
and `RESEARCH-METHOD.md` already records that marketplace price taxes
conversion rather than capping it.

But the question was pointing at something real that our gates had missed.

## The actual test: can the buyer price this item already?

Some products are **recognisable** — the buyer has bought one, seen one, and
carries a price. Others are **unfamiliar**, with no stored reference.

A 4-section plastic masala box is recognisable. A USB rechargeable electric
garlic chopper is not. Both are cheap for us; only one of them lets us set a
price.

So the measurable form of the test is: **does our price sit inside the range
the buyer already sees on a marketplace?** Not "are we cheaper" — inside.

## Measured, Meesho, 20 listings each, 2026-10-12

| id | product | our cost | Meesho median | Meesho range | our price | multiple | inside range? |
|---|---|---|---|---|---|---|---|
| C016 | USB garlic chopper | Rs 159 | Rs 543 | Rs 127 - 1,604 | Rs 1,299 | 2.4x | **YES** |
| C019 | masala box | Rs 74 | Rs 180 | Rs 110 - 960 | Rs 1,199 | 6.7x | no |
| C017 | silicone stretch lids | Rs 96 | Rs 149 | Rs 96 - 389 | Rs 1,199 | 8.0x | no |
| C021 | electric spin scrubber | Rs 911 | Rs 924 | Rs 796 - 977 | Rs 2,499 | 2.7x | no |

Multiple alone does not decide it — C016 at 2.4x passes and C021 at 2.7x
fails. What separates them is whether the price lands inside a range buyers
already accept. C016 at Rs 1,299 is the premium end of a market that visibly
runs to Rs 1,604. C021 at Rs 2,499 is 2.5x above the dearest listing anyone
on the platform manages.

## The squeeze, confirmed again

C019 at a credible price [computed]:

| selling price | break-even CPP |
|---|---|
| Rs 499 (2.8x median, about as far as a masala box stretches) | **Rs 174** |
| Rs 699 | Rs 301 |
| Rs 1,199 (what the economics wanted) | Rs 618 |

Real Indian CPP is Rs 200-250. At Rs 499 we need Rs 174, so it loses money at
any price a buyer would accept, and only earns at a price they will not pay.
Identical to the C018 failure, reached from the opposite direction: C018 was
anchored by competitors' ads, C019 by the marketplace itself.

## C021 is worse than anchored

Meesho sells the spin scrubber at a median of Rs 924 against our DeoDap cost
of Rs 911. **Sellers there retail it for roughly what we pay.** There is no
version of this where we compete; at market price we are underwater before
any advertising. Blocked, and this time for a measured reason rather than the
wrong one in `CORRECTION-floor-is-not-a-price.md`.

## Gate added to PRODUCT-SELECTION.md

**Gate 4 — perceived value.** Search the product on Meesho, record the median
and the full range of the first 20 listings, and record whether our intended
price sits inside that range.

- Inside the range -> proceed. We are a premium option in a market the buyer
  accepts.
- Outside, but the item is genuinely unfamiliar -> proceed with caution and
  make differentiation explicit.
- Outside, and the item is recognisable -> **blocked**. No creative fixes a
  buyer who knows the thing costs Rs 180.
- Marketplace price at or below our supplier cost -> **blocked outright**.

Cheap supply is not an advantage on its own. Rs 74 looked like the best
economics on the shortlist and was the second-ranked product; it is now
blocked. **Cost does not create willingness to pay.**

## Effect on the shortlist

C016 is the only one of six passing all four gates. That is a thin result,
and it is the honest one — three products were ranked above their evidence
until this check was run.

---

## REVISION, same day — the owner corrected the gate

*"using marketplace median such as meesho is i think too over. Because meesho
is also a wholesaling type of platform, we are playing on creatives and
customer targeting so we also might price our product higher than meesho."*

Correct, and the first version of this gate broke a standing decision. The
decision table already said **marketplace price taxes conversion, it does not
cap our price** — and I turned it into a hard cap keyed to the cheapest
platform in India. That is the second time in this project I have swung to an
extreme on the marketplace-price question.

### What was actually right, and why

The masala box conclusion holds, but for the reason the owner gave: it is a
**very common object and buyers know what it should cost**. Recognisability
is the block. The Meesho multiple was a symptom I mistook for the cause.

The distinction that survives:

- **Competitor ads anchor hard.** They run in the same feed we advertise in.
  C018's buyer sees Rs 399 from eight advertisers in the same scroll.
- **Marketplace listings mostly do not.** Our buyer is not searching Meesho.
  Charging more than Meesho *is* the business model.

### What changed

- **C017 reinstated.** Blocked at 8.0x the Meesho median, which is no longer a
  blocking criterion. Silicone stretch lids are not something most buyers have
  owned, so no price is fixed in their head. Its real risks are unchanged and
  unrelated: a 3.91 DeoDap rating from 35 reviews, and no ad check yet.
- **C019 stays blocked** — recognisable commodity, owner concurs.
- **C021 stays blocked** — Meesho retail (~Rs 924) sits at our supplier cost
  (Rs 911). Arithmetic, not positioning.
- **C018 stays blocked** — ad anchor, which is the kind that counts.

### Lesson worth keeping

A measurement that correlates with a real problem is not the same as the
problem. The Meesho multiple correlated with recognisability across four
products, so it looked like a gate. It was a proxy, and using it as a rule
would have thrown away good products for the wrong reason.
