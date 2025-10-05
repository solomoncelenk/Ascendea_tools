#!/usr/bin/env python3
import argparse, os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

px.defaults.template = "plotly_dark"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--offer", required=True)
    ap.add_argument("--revenue", required=True)
    ap.add_argument("--cogs", required=True)
    ap.add_argument("--date", default=None)
    ap.add_argument("--segment", default=None)
    ap.add_argument("--variable", default=None)
    ap.add_argument("--units", default=None)
    ap.add_argument("--out", default="output")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    charts = os.path.join(args.out, "charts")
    os.makedirs(charts, exist_ok=True)

    if args.input.lower().endswith(".xlsx"):
        df = pd.read_excel(args.input)
    else:
        df = pd.read_csv(args.input)

    for c in [args.revenue, args.cogs] + ([args.variable] if args.variable else []) + ([args.units] if args.units else []):
        if c and c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    if args.date and args.date in df.columns:
        df[args.date] = pd.to_datetime(df[args.date], errors="coerce")

    mask = df[args.offer].notna() & df[args.revenue].notna() & df[args.cogs].notna()
    df = df[mask].copy()

    df["gross_profit"] = df[args.revenue] - df[args.cogs]
    df["gross_margin_pct"] = np.where(df[args.revenue]>0, df["gross_profit"]/df[args.revenue], np.nan)

    if args.variable and args.variable in df.columns:
        df["contribution_profit"] = df["gross_profit"] - df[args.variable].fillna(0)
        df["contribution_margin_pct"] = np.where(df[args.revenue]>0, df["contribution_profit"]/df[args.revenue], np.nan)

    if args.units and args.units in df.columns:
        df["revenue_per_unit"] = np.where(df[args.units]>0, df[args.revenue]/df[args.units], np.nan)
        df["gross_profit_per_unit"] = np.where(df[args.units]>0, df["gross_profit"]/df[args.units], np.nan)

    group_cols = [args.offer] + ([args.segment] if args.segment and args.segment in df.columns else [])
    agg = {args.revenue:"sum", args.cogs:"sum", "gross_profit":"sum"}
    if args.variable and args.variable in df.columns:
        agg["contribution_profit"] = "sum"
    if args.units and args.units in df.columns:
        agg[args.units] = "sum"

    summ = df.groupby(group_cols).agg(agg).reset_index()
    summ["gross_margin_pct"] = np.where(summ[args.revenue]>0, summ["gross_profit"]/summ[args.revenue], np.nan)
    if "contribution_profit" in summ.columns:
        summ["contribution_margin_pct"] = np.where(summ[args.revenue]>0, summ["contribution_profit"]/summ[args.revenue], np.nan)

    summ.to_csv(os.path.join(args.out, "summary.csv"), index=False)

    pareto = summ.sort_values(args.revenue, ascending=False).reset_index(drop=True)
    pareto["cum_revenue"] = pareto[args.revenue].cumsum()
    tot = pareto[args.revenue].sum()
    pareto["cum_share"] = np.where(tot>0, pareto["cum_revenue"]/tot, np.nan)
    pareto.to_csv(os.path.join(args.out, "pareto_revenue.csv"), index=False)

    bar_df = summ.sort_values("gross_profit", ascending=False).head(20)
    fig_bar = px.bar(bar_df, x=args.offer, y="gross_profit", color=args.revenue, title="Top Offers by Gross Profit")
    fig_bar.write_image(os.path.join(charts, "top_offers_gross_profit.png"), scale=2)

    fig_sc = px.scatter(summ, x=args.revenue, y="gross_margin_pct", text=args.offer, size="gross_profit", size_max=40, title="Revenue vs Gross Margin %")
    fig_sc.write_image(os.path.join(charts, "revenue_vs_margin.png"), scale=2)

    fig_p = px.line(pareto.reset_index(), x="index", y="cum_share", markers=True, title="Cumulative Revenue Share by Ranked Offer")
    fig_p.add_hline(y=0.8, line_dash="dash")
    fig_p.write_image(os.path.join(charts, "pareto_curve.png"), scale=2)

    if args.date and args.date in df.columns:
        ts = df.copy()
        ts["_month"] = ts[args.date].dt.to_period("M").dt.to_timestamp()
        ts_g = ts.groupby("_month").agg({args.revenue:"sum","gross_profit":"sum"}).reset_index()
        fig_ts = px.line(ts_g, x="_month", y=[args.revenue,"gross_profit"], markers=True, title="Revenue & Gross Profit by Month")
        fig_ts.write_image(os.path.join(charts, "monthly_trends.png"), scale=2)

    print("Done. Outputs saved to", args.out)

if __name__ == "__main__":
    main()
