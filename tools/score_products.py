#!/usr/bin/env python3
"""
Score a supplier catalog export and rank candidates.

Takes the boring, mechanical half of product research off the table: hard
filters, pricing, shipping class and unit economics for every row, applied
identically. What it CANNOT judge is whether a product stops a thumb on a
Reel, or how crowded it already is -- those need research per candidate
and are left as blank columns for exactly that reason.

The point is to turn 3,000 catalog rows into 20 worth researching, not to
pick the winner.

Usage:
  python3 score_products.py data/catalog/deodap.csv
  python3 score_products.py data/catalog/deodap.csv --top 30 --out data/scored.csv

Input CSV needs at least: name, cost. Optional and used if present:
  weight_g, category, moq, stock, url, material, length_cm
See data/catalog/TEMPLATE.csv.
"""

import argparse, csv, math, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unit_economics import economics

PRICE_FLOOR = 1099      # PLAN.md section 2; set by CPP headroom, not by GST
GST_RATE = 0.0          # NOT GST-registered; see PLAN.md section 2d
MARKUP = 3.2            # typical sustainable markup on low-ticket decor
MIN_TARGET_CPP = 280    # below this, Meta CPP in India eats the product

FRAGILE = r"glass|ceramic|mirror|resin|marble|porcelain|crystal|terracotta|clay|stoneware"
ELECTRICAL = r"electric|led|lamp|light|plug|battery|charger|motor|usb|bulb|heater"
SIZING = r"size|fit|\bsize\b|curtain size|cover size"
EXCLUDE_CAT = r"idol|god|deity|religious|puja|candle|diffuser|perfume|fragrance"


def shipping_for(weight_g):
    """Courier slab cost per leg, India surface, rough but directionally right."""
    if weight_g is None:
        return 70, "unknown"
    for limit, cost, label in ((500, 70, "<=500g"), (1000, 100, "<=1kg"),
                               (2000, 150, "<=2kg"), (5000, 260, "<=5kg")):
        if weight_g <= limit:
            return cost, label
    return 400, ">5kg"


def num(row, *keys):
    for k in keys:
        v = (row.get(k) or "").strip().replace(",", "").replace("Rs", "").replace("₹", "")
        if v:
            try:
                return float(re.sub(r"[^\d.]", "", v) or 0) or None
            except ValueError:
                pass
    return None


def suggest_price(cost):
    """Price to the floor, via a markup, landing on a .99 point."""
    raw = max(cost * MARKUP, PRICE_FLOOR)
    bundle = 1
    if cost * MARKUP < PRICE_FLOOR:
        # Too cheap alone -- bundle until the markup clears the floor by itself.
        bundle = max(2, math.ceil(PRICE_FLOOR / (cost * MARKUP)))
        raw = cost * bundle * MARKUP
    return round(raw / 100) * 100 - 1, bundle


def hard_filters(row, name, cost, weight_g):
    """Reasons to reject outright. Empty list means it survives."""
    blob = " ".join(str(v) for v in row.values()).lower()
    out = []
    if re.search(FRAGILE, blob):
        out.append("fragile")
    if re.search(ELECTRICAL, blob):
        out.append("electrical")
    if re.search(EXCLUDE_CAT, blob):
        out.append("excluded-category")
    if re.search(SIZING, blob):
        out.append("sizing-risk")
    if weight_g and weight_g > 2000:
        out.append("too-heavy")
    if (ln := num(row, "length_cm", "length", "size_cm")) and ln > 45:
        out.append("too-bulky")
    if not cost:
        out.append("no-cost")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("catalog")
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--out", default="data/scored.csv")
    ap.add_argument("--rto", type=float, default=0.30)
    ap.add_argument("--show-rejects", action="store_true")
    a = ap.parse_args()

    with open(a.catalog, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        sys.exit(f"No rows in {a.catalog}")

    kept, rejected = [], []
    for row in rows:
        name = (row.get("name") or row.get("title") or row.get("product") or "").strip()
        if not name:
            continue
        cost = num(row, "cost", "price", "supplier_price", "cost_price")
        weight_g = num(row, "weight_g", "weight", "weight_grams")

        reasons = hard_filters(row, name, cost, weight_g)
        if reasons:
            rejected.append((name, ", ".join(reasons)))
            continue

        ship, slab = shipping_for(weight_g)
        sp, bundle = suggest_price(cost)
        unit_cogs = cost * bundle

        e = economics(sp=sp, cogs=unit_cogs, ship_fwd=ship, ship_rto=ship,
                      cod_fee=40, pg_fee_pct=0.02, rto_rate=a.rto,
                      prepaid_share=0.20, prepaid_return_rate=0.04,
                      restock_loss=0.15, gst_rate=GST_RATE)
        be_cpp = e["contribution"]
        target_cpp = be_cpp * 0.70

        if target_cpp < MIN_TARGET_CPP:
            rejected.append((name, f"thin margin (target CPP Rs {target_cpp:.0f})"))
            continue

        kept.append({
            "name": name,
            "category": (row.get("category") or "").strip(),
            "supplier_cost": round(cost),
            "bundle_qty": bundle,
            "suggested_sp": sp,
            "weight_g": int(weight_g) if weight_g else "",
            "ship_slab": slab,
            "ship_per_leg": ship,
            "breakeven_cpp": round(be_cpp),
            "target_cpp": round(target_cpp),
            "kill_at_spend": round(be_cpp * 2.5),
            "url": (row.get("url") or "").strip(),
            # Filled by research, not by this script:
            "visual_hook": "",
            "problem_solved": "",
            "saturation": "",
            "verdict": "",
        })

    kept.sort(key=lambda r: r["target_cpp"], reverse=True)

    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(kept[0].keys()) if kept else ["name"])
        w.writeheader()
        w.writerows(kept)

    print(f"\n  {len(rows)} rows in -> {len(kept)} survive, {len(rejected)} rejected")
    print(f"  Shortlist written to {a.out}\n")
    print(f"  {'Product':<42}{'Cost':>6}{'Qty':>5}{'SP':>7}{'TgtCPP':>8}{'Kill@':>7}")
    print("  " + "-" * 75)
    for r in kept[:a.top]:
        nm = r["name"][:40]
        print(f"  {nm:<42}{r['supplier_cost']:>6}{r['bundle_qty']:>5}"
              f"{r['suggested_sp']:>7}{r['target_cpp']:>8}{r['kill_at_spend']:>7}")
    print("  " + "-" * 75)
    print(f"  Qty = units to bundle to clear the Rs {PRICE_FLOOR} floor.")
    print("  TgtCPP = most you should pay per purchase. Kill@ = spend with no sale -> stop.")
    print("\n  Columns visual_hook / problem_solved / saturation / verdict are")
    print("  deliberately empty. Economics cannot tell you if a product sells;")
    print("  those need per-product research. Next: research the top rows.\n")

    if a.show_rejects:
        print("  Rejected:")
        for n, why in rejected[:40]:
            print(f"    {n[:50]:<52} {why}")
        print()


if __name__ == "__main__":
    main()
