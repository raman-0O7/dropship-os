#!/usr/bin/env python3
"""
Unit economics for India COD dropshipping.

Answers the only two questions that matter before you spend on ads:
  1. How much money does one order actually leave you, before ad spend?
  2. What is the highest cost-per-purchase (CPP) you can pay and still break even?

Everything is computed PER ORDER PLACED, not per delivered order, because you
pay Meta for every order including the ones that come back as RTO.

Usage:
  python3 unit_economics.py --sp 599 --cogs 180
  python3 unit_economics.py --sp 599 --cogs 180 --sensitivity
  python3 unit_economics.py --sp 999 --cogs 320 --rto 0.35 --prepaid-share 0.15
"""

import argparse


def economics(sp, cogs, ship_fwd, ship_rto, cod_fee, pg_fee_pct,
              rto_rate, prepaid_share, prepaid_return_rate, restock_loss,
              gst_rate=0.0, service_gst=0.18):
    """Contribution per order placed, before ad spend.

    gst_rate > 0 means we are GST-registered. Every rupee passed in is then
    treated as GST-inclusive and the tax is stripped out, because collected
    GST is the government's money, not ours -- and the GST we paid on the
    product, shipping and fees comes back as input credit.

    Net effect: GST costs roughly rate/(1+rate) of gross margin, about 15%
    at an 18% rate. It is NOT 18% of revenue, and it is NOT 18% of profit.
    """
    if gst_rate:
        sp = sp / (1 + gst_rate)
        cogs = cogs / (1 + gst_rate)
        ship_fwd = ship_fwd / (1 + service_gst)
        ship_rto = ship_rto / (1 + service_gst)
        cod_fee = cod_fee / (1 + service_gst)

    cod_share = 1.0 - prepaid_share

    # --- Prepaid leg ---
    pg_fee = sp * pg_fee_pct
    prepaid_kept = sp - cogs - ship_fwd - pg_fee
    # A prepaid return: refund the customer, eat shipping both ways + restock loss.
    prepaid_returned = -(ship_fwd + ship_rto) - cogs * restock_loss - pg_fee
    prepaid_value = ((1 - prepaid_return_rate) * prepaid_kept
                     + prepaid_return_rate * prepaid_returned)

    # --- COD leg ---
    cod_delivered = sp - cogs - ship_fwd - cod_fee
    # RTO: no revenue, product comes back to supplier, you eat both legs of
    # shipping plus whatever the supplier does not credit back (restock_loss).
    cod_rto = -(ship_fwd + ship_rto) - cogs * restock_loss
    cod_value = (1 - rto_rate) * cod_delivered + rto_rate * cod_rto

    contribution = prepaid_share * prepaid_value + cod_share * cod_value

    return {
        "prepaid_kept": prepaid_kept,
        "prepaid_returned": prepaid_returned,
        "prepaid_value": prepaid_value,
        "cod_delivered": cod_delivered,
        "cod_rto": cod_rto,
        "cod_value": cod_value,
        "contribution": contribution,
    }


def fmt(x):
    return f"Rs {x:,.0f}"


def report(args):
    e = economics(args.sp, args.cogs, args.ship_fwd, args.ship_rto,
                  args.cod_fee, args.pg_fee, args.rto, args.prepaid_share,
                  args.prepaid_return, args.restock_loss, args.gst)

    breakeven_cpp = e["contribution"]
    # Meta charges 18% GST on ads. Registered, we reclaim it, so the quoted
    # CPP is spendable in full. Unregistered, it is a real 18% surcharge.
    ad_gst_factor = 1.0 if args.gst else 1.18
    breakeven_cpp = breakeven_cpp / ad_gst_factor
    # Target CPP leaves you a real margin, not just break-even.
    target_cpp = breakeven_cpp * (1 - args.target_margin)
    kill_spend = args.kill_multiple * breakeven_cpp

    print()
    print("=" * 62)
    reg = f"GST-registered @ {args.gst:.0%}" if args.gst else "not GST-registered"
    print(f"  SP {fmt(args.sp)}  |  COGS {fmt(args.cogs)}  |  "
          f"RTO {args.rto:.0%}  |  prepaid {args.prepaid_share:.0%}")
    print(f"  {reg}; ad GST {'reclaimed' if args.gst else 'absorbed (+18% on ads)'}")
    print("=" * 62)
    print()
    print("  Per order placed, before ad spend")
    print("  " + "-" * 44)
    print(f"  COD delivered  ({(1-args.rto)*100:4.0f}% of COD)   "
          f"{fmt(e['cod_delivered']):>12}")
    print(f"  COD returned   ({args.rto*100:4.0f}% of COD)   "
          f"{fmt(e['cod_rto']):>12}")
    print(f"  Prepaid order                     {fmt(e['prepaid_value']):>12}")
    print("  " + "-" * 44)
    print(f"  Blended contribution              {fmt(e['contribution']):>12}")
    print()

    if breakeven_cpp <= 0:
        print("  !! This product loses money at ZERO ad spend.")
        print("     RTO and shipping eat the whole margin. Do not test it.")
        print("     Fixes: raise price, cut COD share, or pick a cheaper-to-ship product.")
        print()
        return

    print("  Your rules")
    print("  " + "-" * 44)
    print(f"  Break-even CPP                    {fmt(breakeven_cpp):>12}")
    print(f"  Target CPP ({args.target_margin:.0%} margin)         "
          f"{fmt(target_cpp):>12}")
    print(f"  KILL at spend with 0 orders       {fmt(kill_spend):>12}")
    profit_at_target = e["contribution"] - target_cpp * ad_gst_factor
    print(f"  Profit per order at target CPP    {fmt(profit_at_target):>12}")
    print()
    print(f"  Meaning: if Meta charges you more than {fmt(breakeven_cpp)} per")
    print(f"  purchase, you are paying to lose money. Aim under {fmt(target_cpp)}.")
    print(f"  If you have spent {fmt(kill_spend)} on this product with no sale,")
    print("  the CPP is almost certainly above break-even. Stop it.")
    print()


def sensitivity(args):
    print("  Break-even CPP as RTO and prepaid share move")
    print("  (rows = RTO rate, cols = share of orders that are prepaid)")
    print()
    shares = [0.0, 0.15, 0.30, 0.50]
    header = "  RTO  " + "".join(f"{s:>10.0%}" for s in shares)
    print(header)
    print("  " + "-" * (len(header) - 2))
    for rto in [0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.50]:
        row = f"  {rto:>4.0%} "
        for s in shares:
            c = economics(args.sp, args.cogs, args.ship_fwd, args.ship_rto,
                          args.cod_fee, args.pg_fee, rto, s,
                          args.prepaid_return, args.restock_loss,
                          args.gst)["contribution"]
            row += f"{c:>10,.0f}" if c > 0 else f"{'LOSS':>10}"
        print(row)
    print()
    print("  Every rupee you move from COD to prepaid, and every point of RTO")
    print("  you prevent, raises the CPP you can afford. That is why the COD")
    print("  confirmation flow is the highest-value thing to automate.")
    print()


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--sp", type=float, required=True,
                   help="selling price incl. any shipping you charge the customer")
    p.add_argument("--cogs", type=float, required=True,
                   help="supplier price per unit (DeoDap landed cost)")
    p.add_argument("--ship-fwd", type=float, default=70,
                   help="forward shipping cost you pay (default 70)")
    p.add_argument("--ship-rto", type=float, default=70,
                   help="return shipping cost on an RTO (default 70)")
    p.add_argument("--cod-fee", type=float, default=40,
                   help="COD remittance fee per delivered order (default 40)")
    p.add_argument("--pg-fee", type=float, default=0.02,
                   help="payment gateway fee on prepaid, as a fraction (default 0.02)")
    p.add_argument("--rto", type=float, default=0.30,
                   help="fraction of COD orders returned to origin (default 0.30)")
    p.add_argument("--prepaid-share", type=float, default=0.20,
                   help="fraction of orders that are prepaid (default 0.20)")
    p.add_argument("--prepaid-return", type=float, default=0.04,
                   help="return rate on prepaid orders (default 0.04)")
    p.add_argument("--restock-loss", type=float, default=0.15,
                   help="fraction of COGS you do NOT recover on a return, "
                        "e.g. damage or supplier restocking fee (default 0.15)")
    p.add_argument("--target-margin", type=float, default=0.30,
                   help="margin to keep after ads, as a fraction (default 0.30)")
    p.add_argument("--kill-multiple", type=float, default=2.5,
                   help="kill a product after this many break-even CPPs of "
                        "spend with no sale (default 2.5)")
    p.add_argument("--gst", type=float, default=0.0,
                   help="output GST rate on the product if we are registered, "
                        "e.g. 0.18. Treats all amounts as GST-inclusive. "
                        "0 (default) means not registered")
    p.add_argument("--sensitivity", action="store_true",
                   help="also print the RTO / prepaid sensitivity table")
    args = p.parse_args()

    report(args)
    if args.sensitivity:
        sensitivity(args)


if __name__ == "__main__":
    main()
