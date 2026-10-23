#!/usr/bin/env python3
"""
Compare COD checkout policies, accounting for the conversion they cost you.

The trap in this decision is comparing RTO rates. A policy that adds
checkout friction wins on RTO and can still lose money, because ad spend
buys visitors, not orders -- so fewer orders at the same ad spend means a
higher cost per order.

The number that actually decides it: how much of your order volume a
policy can destroy before it is worse than doing nothing. Call it the
conversion cushion. If you believe the real-world friction costs less
than the cushion, adopt the policy.

Usage:
  python3 cod_policy.py --sp 599 --cogs 180
  python3 cod_policy.py --sp 899 --cogs 280 --advance 149
"""

import argparse


def legs(sp, cogs, ship_fwd, ship_rto, cod_fee, pg_fee_pct, restock_loss):
    """Per-order value of each possible order type and outcome."""
    return {
        "prepaid_kept": sp - cogs - ship_fwd - sp * pg_fee_pct,
        "cod_delivered": sp - cogs - ship_fwd - cod_fee,
        "rto": -(ship_fwd + ship_rto) - cogs * restock_loss,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--sp", type=float, required=True)
    p.add_argument("--cogs", type=float, required=True)
    p.add_argument("--ship-fwd", type=float, default=70)
    p.add_argument("--ship-rto", type=float, default=70)
    p.add_argument("--cod-fee", type=float, default=40)
    p.add_argument("--pg-fee", type=float, default=0.02)
    p.add_argument("--restock-loss", type=float, default=0.15)
    p.add_argument("--rto", type=float, default=0.30,
                   help="RTO rate on plain zero-commitment COD (default 0.30)")
    p.add_argument("--prepaid-share", type=float, default=0.20,
                   help="baseline share of orders that are prepaid (default 0.20)")
    p.add_argument("--prepaid-return", type=float, default=0.04)
    p.add_argument("--discount", type=float, default=0.05,
                   help="prepaid discount offered, as a fraction (default 0.05)")
    p.add_argument("--discount-shift", type=float, default=0.15,
                   help="extra share of orders the discount pulls from COD to "
                        "prepaid (default 0.15)")
    p.add_argument("--advance", type=float, default=99,
                   help="partial-COD advance collected online (default 99)")
    p.add_argument("--advance-rto", type=float, default=0.10,
                   help="RTO rate once an advance is paid (default 0.10)")
    a = p.parse_args()

    L = legs(a.sp, a.cogs, a.ship_fwd, a.ship_rto, a.cod_fee, a.pg_fee, a.restock_loss)

    # Order types, expected value each
    ev_prepaid = (1 - a.prepaid_return) * L["prepaid_kept"] + a.prepaid_return * L["rto"]
    ev_cod = (1 - a.rto) * L["cod_delivered"] + a.rto * L["rto"]

    sp_d = a.sp * (1 - a.discount)
    Ld = legs(sp_d, a.cogs, a.ship_fwd, a.ship_rto, a.cod_fee, a.pg_fee, a.restock_loss)
    ev_prepaid_disc = ((1 - a.prepaid_return) * Ld["prepaid_kept"]
                       + a.prepaid_return * Ld["rto"])

    # Partial COD: advance is collected online and kept if the parcel is refused.
    adv_net = a.advance * (1 - a.pg_fee)
    ev_partial = ((1 - a.advance_rto) * (L["cod_delivered"] - a.advance * a.pg_fee)
                  + a.advance_rto * (L["rto"] + adv_net))

    print(f"\n  Rs {a.sp:,.0f} product | plain-COD RTO {a.rto:.0%} | "
          f"advance Rs {a.advance:,.0f} at {a.advance_rto:.0%} RTO\n")
    print("  Expected value of ONE order, by type")
    print("  " + "-" * 50)
    print(f"  Prepaid, full price                  Rs {ev_prepaid:>7,.0f}")
    print(f"  Prepaid, {a.discount:.0%} discount                Rs {ev_prepaid_disc:>7,.0f}")
    print(f"  Partial COD (Rs {a.advance:,.0f} advance)        Rs {ev_partial:>7,.0f}")
    print(f"  Plain COD, zero commitment           Rs {ev_cod:>7,.0f}")
    print()

    # --- Policies, blended per order, ad spend held FIXED ---
    pre, cod = a.prepaid_share, 1 - a.prepaid_share
    baseline = pre * ev_prepaid + cod * ev_cod

    shift = min(a.discount_shift, cod)
    discount_policy = ((pre + shift) * ev_prepaid_disc + (cod - shift) * ev_cod)

    partial_policy = pre * ev_prepaid + cod * ev_partial
    both = ((pre + shift) * ev_prepaid_disc + (cod - shift) * ev_partial)

    print("  Policy comparison, blended per order")
    print("  " + "-" * 62)
    print(f"  {'Policy':<34}{'Per order':>12}{'Cushion':>14}")
    print("  " + "-" * 62)
    for name, val in [("A. Nothing (plain COD)", baseline),
                      (f"B. Prepaid {a.discount:.0%} discount only", discount_policy),
                      ("C. Partial COD only", partial_policy),
                      ("D. Both", both)]:
        if val <= baseline:
            cush = "worse"
        else:
            cush = f"{1 - baseline / val:.0%} of orders"
        mark = "  <-- base" if name.startswith("A") else ""
        print(f"  {name:<34}Rs {val:>8,.0f}{cush:>14}{mark}")
    print("  " + "-" * 62)
    print()
    print("  Cushion = the share of your order volume that policy can destroy")
    print("  before it earns you less than doing nothing, at the same ad spend.")
    print()


if __name__ == "__main__":
    main()
 
