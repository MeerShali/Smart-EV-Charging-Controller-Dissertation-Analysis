"""
Energy Price Analysis - Multi-panel Visualization

Generates comparative time series, hourly profiles, and distributions
for Germany-Luxembourg energy prices (2025-2026).

@author: Meer Shali
@year: 2026
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Patch
from . import utils

# ─── Configuration ─────────────────────────────────────────────────────────

OUTPUT_DIR = utils.get_figures_dir() / "energy_analysis"
DATA_DIR = utils.get_data_dir() / "energy_prices"

BLUE = utils.BLUE
ORANGE = utils.ORANGE
BACKGROUND = utils.BACKGROUND

# ─── Functions ─────────────────────────────────────────────────────────────

def load_csv(path):
    """
    Load and parse energy price CSV.
    
    Handles:
    - MTU (Market Time Unit) parsing
    - Unit conversion (EUR/MWh → EUR/kWh if needed)
    - Missing value removal
    """
    df = pd.read_csv(path)
    
    # Find MTU and price columns
    mtu_col = next(c for c in df.columns if c.startswith("MTU"))
    price_col = next(c for c in df.columns if "Day-ahead Price" in c)
    
    # Parse timestamp from MTU
    start = df[mtu_col].str.split(" - ").str[0]
    start = start.str.replace(r"\s*\([^)]+\)$", "", regex=True).str.strip()
    df["ts"] = pd.to_datetime(start, dayfirst=True)
    
    # Normalize price to EUR/kWh
    df["price"] = df[price_col] * (1 if "kWh" in price_col else 0.001)
    
    return df[["ts", "price"]].dropna()

def make_year_figure(df, title, filename):
    """
    Generate 5-panel annual analysis figure.
    
    Panels:
    1. 15-minute time series
    2. Daily average
    3. Hourly profile with min/max band
    4. Price distribution histogram
    5. Monthly box plots
    """
    df = df.copy()
    df["month"] = df["ts"].dt.to_period("M")
    months = sorted(df["month"].unique())
    month_labels = [str(m) for m in months]
    
    fig = plt.figure(figsize=(20, 17), facecolor="white")
    fig.suptitle(
        f"Germany-Luxembourg Energy Prices (BZN|DE-LU)\n{title}",
        fontsize=16, fontweight="bold", y=0.98,
    )
    gs = GridSpec(3, 2, figure=fig, hspace=0.42, wspace=0.28,
                  left=0.06, right=0.97, top=0.92, bottom=0.05)
    
    ax_ts = fig.add_subplot(gs[0, :])
    ax_daily = fig.add_subplot(gs[1, 0])
    ax_hour = fig.add_subplot(gs[1, 1])
    ax_dist = fig.add_subplot(gs[2, 0])
    ax_box = fig.add_subplot(gs[2, 1])
    
    # Panel 1: 15-min time series
    ax_ts.set_title("15-Minute Day-Ahead Prices", fontsize=11)
    sub = df.sort_values("ts")
    ax_ts.plot(sub["ts"], sub["price"], color=BLUE, linewidth=0.5, alpha=0.85)
    ax_ts.axhline(0, color="gray", linewidth=0.7, linestyle="--")
    ax_ts.set_ylabel("EUR/kWh", fontsize=9)
    ax_ts.xaxis.set_major_locator(mdates.MonthLocator())
    ax_ts.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.setp(ax_ts.xaxis.get_majorticklabels(), rotation=0, ha="center", fontsize=8)
    ax_ts.set_facecolor("#f8f8f8")
    ax_ts.grid(axis="y", color="white", linewidth=0.8)
    
    # Panel 2: Daily average
    ax_daily.set_title("Daily Average Price", fontsize=11)
    daily = df.groupby(df["ts"].dt.date)["price"].mean()
    daily.index = pd.to_datetime(daily.index)
    ax_daily.plot(daily.index, daily.values, color=BLUE, linewidth=1.2)
    ax_daily.axhline(0, color="gray", linewidth=0.7, linestyle="--")
    ax_daily.set_ylabel("EUR/kWh", fontsize=9)
    ax_daily.xaxis.set_major_locator(mdates.MonthLocator())
    ax_daily.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    plt.setp(ax_daily.xaxis.get_majorticklabels(), rotation=0, ha="center", fontsize=8)
    ax_daily.set_facecolor("#f8f8f8")
    ax_daily.grid(axis="y", color="white", linewidth=0.8)
    
    # Panel 3: Hourly profile
    ax_hour.set_title("Average Price by Hour of Day", fontsize=11)
    df["hour"] = df["ts"].dt.hour
    hourly_mean = df.groupby("hour")["price"].mean()
    hourly_min = df.groupby("hour")["price"].min()
    hourly_max = df.groupby("hour")["price"].max()
    ax_hour.fill_between(hourly_mean.index, hourly_min, hourly_max, alpha=0.12, color=BLUE)
    ax_hour.plot(hourly_mean.index, hourly_mean.values, color=BLUE, marker="o", markersize=3.5, linewidth=1.5)
    ax_hour.set_xlabel("Hour (CET)", fontsize=9)
    ax_hour.set_ylabel("EUR/kWh", fontsize=9)
    ax_hour.set_xticks(range(0, 24, 2))
    ax_hour.set_facecolor("#f8f8f8")
    ax_hour.grid(axis="y", color="white", linewidth=0.8)
    
    # Panel 4: Distribution
    ax_dist.set_title("Price Distribution", fontsize=11)
    bins = np.linspace(df["price"].quantile(0.005), df["price"].quantile(0.995), 60)
    ax_dist.hist(df["price"], bins=bins, color=BLUE, alpha=0.75, edgecolor="none")
    ax_dist.set_xlabel("EUR/kWh", fontsize=9)
    ax_dist.set_ylabel("Count", fontsize=9)
    ax_dist.set_facecolor("#f8f8f8")
    ax_dist.grid(axis="y", color="white", linewidth=0.8)
    
    # Panel 5: Monthly box plots
    ax_box.set_title("Monthly Price Spread", fontsize=11)
    groups = [df[df["month"] == m]["price"].values for m in months]
    ax_box.boxplot(
        groups, tick_labels=month_labels, patch_artist=True,
        medianprops=dict(color="white", linewidth=1.5),
        flierprops=dict(marker="o", markersize=2, alpha=0.4, markerfacecolor=BLUE, markeredgecolor="none"),
        whiskerprops=dict(color="#333"), capprops=dict(color="#333"),
        boxprops=dict(facecolor=BLUE, color=BLUE),
    )
    ax_box.axhline(0, color="gray", linewidth=0.7, linestyle="--")
    ax_box.set_ylabel("EUR/kWh", fontsize=9)
    plt.setp(ax_box.xaxis.get_majorticklabels(), fontsize=7, rotation=30, ha="right")
    ax_box.set_facecolor("#f8f8f8")
    ax_box.grid(axis="y", color="white", linewidth=0.8)
    
    fig.savefig(filename, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"✓ Saved: {filename}")

def make_combined_figure(df25, df26, filename):
    """
    Generate 2025 vs 2026 comparison figure (5 panels).
    Aligns both years to day-of-year for fair comparison.
    """
    def to_doy(df, ref_year=2000):
        d = df.copy()
        d["ts_aligned"] = d["ts"].apply(lambda t: t.replace(year=ref_year))
        return d
    
    a25 = to_doy(df25)
    a26 = to_doy(df26)
    
    all_months_26 = sorted(df26["ts"].dt.to_period("M").unique())
    
    fig = plt.figure(figsize=(20, 17), facecolor="white")
    fig.suptitle(
        "Germany-Luxembourg Energy Prices (BZN|DE-LU)\n2025 vs 2026 Comparison",
        fontsize=16, fontweight="bold", y=0.98,
    )
    gs = GridSpec(3, 2, figure=fig, hspace=0.42, wspace=0.28,
                  left=0.06, right=0.97, top=0.92, bottom=0.05)
    
    ax_ts = fig.add_subplot(gs[0, :])
    ax_daily = fig.add_subplot(gs[1, 0])
    ax_hour = fig.add_subplot(gs[1, 1])
    ax_dist = fig.add_subplot(gs[2, 0])
    ax_box = fig.add_subplot(gs[2, 1])
    
    legend_patches = [
        Patch(color=BLUE, label="2025"),
        Patch(color=ORANGE, label="2026"),
    ]
    
    # Panel 1: Time series (day-of-year aligned)
    ax_ts.set_title("15-Minute Day-Ahead Prices (Day-of-Year Aligned)", fontsize=11)
    for ds, color, lbl in [(a25, BLUE, "2025"), (a26, ORANGE, "2026")]:
        s = ds.sort_values("ts_aligned")
        ax_ts.plot(s["ts_aligned"], s["price"], color=color, linewidth=0.5, alpha=0.8, label=lbl)
    ax_ts.axhline(0, color="gray", linewidth=0.7, linestyle="--")
    ax_ts.set_ylabel("EUR/kWh", fontsize=9)
    ax_ts.xaxis.set_major_locator(mdates.MonthLocator())
    ax_ts.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    plt.setp(ax_ts.xaxis.get_majorticklabels(), rotation=0, ha="center", fontsize=9)
    ax_ts.legend(handles=legend_patches, fontsize=10, loc="upper right")
    ax_ts.set_facecolor("#f8f8f8")
    ax_ts.grid(axis="y", color="white", linewidth=0.8)
    
    # Panel 2: Daily average
    ax_daily.set_title("Daily Average Price", fontsize=11)
    for ds, color, lbl in [(a25, BLUE, "2025"), (a26, ORANGE, "2026")]:
        daily = ds.groupby(ds["ts_aligned"].dt.date)["price"].mean()
        daily.index = pd.to_datetime(daily.index)
        ax_daily.plot(daily.index, daily.values, color=color, linewidth=1.2, label=lbl)
    ax_daily.axhline(0, color="gray", linewidth=0.7, linestyle="--")
    ax_daily.set_ylabel("EUR/kWh", fontsize=9)
    ax_daily.xaxis.set_major_locator(mdates.MonthLocator())
    ax_daily.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    plt.setp(ax_daily.xaxis.get_majorticklabels(), rotation=0, ha="center", fontsize=8)
    ax_daily.legend(handles=legend_patches, fontsize=9, loc="upper right")
    ax_daily.set_facecolor("#f8f8f8")
    ax_daily.grid(axis="y", color="white", linewidth=0.8)
    
    # Panel 3: Hourly
    ax_hour.set_title("Average Price by Hour of Day", fontsize=11)
    for ds, color, lbl in [(df25, BLUE, "2025"), (df26, ORANGE, "2026")]:
        h = ds.copy()
        h["hour"] = h["ts"].dt.hour
        hmean = h.groupby("hour")["price"].mean()
        ax_hour.plot(hmean.index, hmean.values, color=color, marker="o", markersize=3.5, linewidth=1.5, label=lbl)
    ax_hour.set_xlabel("Hour (CET)", fontsize=9)
    ax_hour.set_ylabel("EUR/kWh", fontsize=9)
    ax_hour.set_xticks(range(0, 24, 2))
    ax_hour.legend(handles=legend_patches, fontsize=9, loc="upper right")
    ax_hour.set_facecolor("#f8f8f8")
    ax_hour.grid(axis="y", color="white", linewidth=0.8)
    
    # Panel 4: Distribution
    ax_dist.set_title("Price Distribution", fontsize=11)
    combined = pd.concat([df25["price"], df26["price"]])
    bins = np.linspace(combined.quantile(0.005), combined.quantile(0.995), 60)
    ax_dist.hist(df25["price"], bins=bins, color=BLUE, alpha=0.65, edgecolor="none", label="2025")
    ax_dist.hist(df26["price"], bins=bins, color=ORANGE, alpha=0.65, edgecolor="none", label="2026")
    ax_dist.set_xlabel("EUR/kWh", fontsize=9)
    ax_dist.set_ylabel("Count", fontsize=9)
    ax_dist.legend(handles=legend_patches, fontsize=9, loc="upper right")
    ax_dist.set_facecolor("#f8f8f8")
    ax_dist.grid(axis="y", color="white", linewidth=0.8)
    
    # Panel 5: Monthly box plots
    ax_box.set_title("Monthly Price Spread (2025 vs 2026)", fontsize=11)
    overlap_months = [m for m in all_months_26]
    month_names = [m.strftime("%b") for m in pd.PeriodIndex(overlap_months).to_timestamp()]
    
    positions_25 = [i * 3 - 0.6 for i in range(1, len(overlap_months) + 1)]
    positions_26 = [i * 3 + 0.6 for i in range(1, len(overlap_months) + 1)]
    tick_pos = [i * 3 for i in range(1, len(overlap_months) + 1)]
    
    def bp_data(df, months):
        return [df[df["ts"].dt.month == m.month]["price"].values for m in months]
    
    for positions, data, color in [
        (positions_25, bp_data(df25, overlap_months), BLUE),
        (positions_26, bp_data(df26, overlap_months), ORANGE),
    ]:
        ax_box.boxplot(
            data, positions=positions, widths=1.0, patch_artist=True,
            medianprops=dict(color="white", linewidth=1.5),
            flierprops=dict(marker="o", markersize=2, alpha=0.35, markerfacecolor=color, markeredgecolor="none"),
            whiskerprops=dict(color="#333"), capprops=dict(color="#333"),
            boxprops=dict(facecolor=color, color=color),
            showfliers=False,
        )
    
    ax_box.set_xticks(tick_pos)
    ax_box.set_xticklabels(month_names, fontsize=8)
    ax_box.axhline(0, color="gray", linewidth=0.7, linestyle="--")
    ax_box.set_ylabel("EUR/kWh", fontsize=9)
    ax_box.legend(handles=legend_patches, fontsize=9, loc="upper right")
    ax_box.set_facecolor("#f8f8f8")
    ax_box.grid(axis="y", color="white", linewidth=0.8)
    
    fig.savefig(filename, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"✓ Saved: {filename}")

if __name__ == "__main__":
    print("📊 Loading energy price data...")
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    df25_path = DATA_DIR / "GUI_ENERGY_PRICES_202412312300-202512312300.csv"
    df26_path = DATA_DIR / "GUI_ENERGY_PRICES_202512312300-202612312300.csv"
    
    if df25_path.exists():
        df25 = load_csv(df25_path)
        print(f"✓ Loaded 2025 data: {len(df25)} records")
    else:
        print(f"⚠️  Warning: {df25_path} not found")
        df25 = None
    
    if df26_path.exists():
        df26 = load_csv(df26_path)
        print(f"✓ Loaded 2026 data: {len(df26)} records")
    else:
        print(f"⚠️  Warning: {df26_path} not found")
        df26 = None
    
    if df25 is not None:
        print("📈 Generating 2025 analysis...")
        make_year_figure(df25, "Jan - Dec 2025", OUTPUT_DIR / "combined_2025.png")
    
    if df26 is not None:
        print("📈 Generating 2026 analysis...")
        make_year_figure(df26, "Jan - Jun 2026", OUTPUT_DIR / "combined_2026.png")
    
    if df25 is not None and df26 is not None:
        print("📈 Generating 2025 vs 2026 comparison...")
        make_combined_figure(df25, df26, OUTPUT_DIR / "combined_2025_2026.png")
    
    print(f"✅ All figures saved to {OUTPUT_DIR}")
