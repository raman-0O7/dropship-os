#!/usr/bin/env python3
"""Look a product up in the DeoDap catalogue and pull the real supplier figures.

This replaces the "we need a catalogue export before we can do economics"
blocker. DeoDap is a Shopify storefront and its product data is public — its
robots.txt states plainly that product HTML is crawlable. We read the same
JSON the storefront itself uses, a handful of requests at a time.

What comes back per product, all of it measured rather than guessed:

  price        supplier cost in rupees
  weight_g     shipping weight, the other half of the economics
  available    in stock right now
  rating       product rating out of 5, and the review count behind it
  sku, vendor, tags, url

One caveat that matters: DeoDap is a SINGLE supplier, not a marketplace.
There are no competing sellers to rank, no per-seller inventory and no public
order counts. `vendor` is a brand label on DeoDap's own catalogue, and
"Seller's choice" is a navigation collection. The rating is the product's,
and it is the closest thing to a quality signal available.

Usage
  tools/deodap_lookup.py "vegetable chopper" "silicone stretch lids"
  tools/deodap_lookup.py --from-csv data/shortlist.csv --column product
  tools/deodap_lookup.py "masala box" --limit 5 --out data/catalog/deodap-matches.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BASE = "https://deodap.in"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "\
     "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
PAUSE = 1.0  # be a polite guest; this is someone else's server

FIELDS = [
    "query", "rank", "title", "price", "weight_g", "available",
    "rating", "review_count", "sku", "vendor", "product_type",
    "sell_rate_tag", "url", "handle",
]


def _get(url: str, timeout: int = 25) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def search(term: str, limit: int = 3) -> list[dict]:
    qs = urllib.parse.urlencode({
        "q": term,
        "resources[type]": "product",
        "resources[limit]": limit,
    })
    try:
        data = json.loads(_get(f"{BASE}/search/suggest.json?{qs}"))
    except Exception as exc:
        print(f"  ! search failed for {term!r}: {exc}", file=sys.stderr)
        return []
    return data.get("resources", {}).get("results", {}).get("products", [])


def product_detail(handle: str) -> dict:
    """Price/weight/sku/tags from the .js endpoint, rating from the HTML."""
    out: dict = {}
    try:
        p = json.loads(_get(f"{BASE}/products/{handle}.js"))
    except Exception as exc:
        print(f"  ! detail failed for {handle}: {exc}", file=sys.stderr)
        return out

    v = (p.get("variants") or [{}])[0]
    out["title"] = p.get("title", "")
    out["price"] = (v.get("price") or 0) / 100
    # Shopify reports `grams` on most stores; DeoDap exposes `weight` only.
    out["weight_g"] = v.get("grams") or v.get("weight") or ""
    out["available"] = p.get("available")
    out["sku"] = v.get("sku", "")
    out["vendor"] = p.get("vendor", "")
    out["product_type"] = p.get("type", "")

    # DeoDap tags its own catalogue with how well a line moves. Worth keeping.
    tags = p.get("tags") or []
    rate = [t for t in tags if t.lower() in ("best selling", "slow sell", "fast sell")]
    out["sell_rate_tag"] = "; ".join(rate)

    time.sleep(PAUSE)
    try:
        html = _get(f"{BASE}/products/{handle}").decode("utf-8", "replace")
        rv = re.search(r'"ratingValue":\s*"?([\d.]+)"?', html)
        rc = re.search(r'"reviewCount":\s*"?(\d+)"?', html)
        out["rating"] = rv.group(1) if rv else ""
        out["review_count"] = rc.group(1) if rc else ""
    except Exception:
        out["rating"] = out["review_count"] = ""
    return out


def lookup(terms: list[str], limit: int) -> list[dict]:
    rows: list[dict] = []
    for term in terms:
        print(f"searching: {term}")
        hits = search(term, limit)
        if not hits:
            print("  no results")
            continue
        for i, h in enumerate(hits, 1):
            time.sleep(PAUSE)
            handle = h.get("handle", "")
            d = product_detail(handle)
            if not d:
                continue
            row = {
                "query": term, "rank": i, "handle": handle,
                "url": f"{BASE}/products/{handle}", **d,
            }
            rows.append({k: row.get(k, "") for k in FIELDS})
            print(
                f"  {i}. Rs {row['price']:>7}  {str(row['weight_g']):>5}g  "
                f"{str(row.get('rating') or '-'):>4}* ({row.get('review_count') or '-'})  "
                f"{'IN STOCK' if row['available'] else 'OUT':8} {row['title'][:46]}"
            )
    return rows


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("terms", nargs="*", help="product descriptions to search for")
    ap.add_argument("--from-csv", help="read search terms from a CSV column")
    ap.add_argument("--column", default="product", help="column to read (default: product)")
    ap.add_argument("--limit", type=int, default=3, help="matches per term (default: 3)")
    ap.add_argument("--out", help="write results to this CSV")
    a = ap.parse_args()

    terms = list(a.terms)
    if a.from_csv:
        with open(a.from_csv, newline="", encoding="utf-8") as fh:
            terms += [r[a.column] for r in csv.DictReader(fh) if r.get(a.column)]
    if not terms:
        ap.error("give at least one search term, or --from-csv")

    rows = lookup(terms, a.limit)
    print(f"\n{len(rows)} match(es) for {len(terms)} term(s)")

    if a.out:
        out = Path(a.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=FIELDS)
            w.writeheader()
            w.writerows(rows)
        print(f"written -> {out}")


if __name__ == "__main__":
    main()
