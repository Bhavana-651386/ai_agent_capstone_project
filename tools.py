import numpy as np
import pandas as pd

# 1️. Trend Analysis (Monthly + KPI Summary)
def analyze_trends(df):

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M")

    monthly = df.groupby(["month", "category"]).agg({
        "units_sold": "sum",
        "revenue": "sum"
    }).reset_index()

    monthly["month"] = monthly["month"].astype(str)

    summary = {
        "total_revenue": round(df["revenue"].sum(), 2),
        "total_units": int(df["units_sold"].sum()),
        "top_category": (
            df.groupby("category")["revenue"]
            .sum()
            .sort_values(ascending=False)
            .index[0]
        )
    }

    return monthly, summary


# 2️. Anomaly Detection (Store-Level)
def detect_anomalies(df):

    df = df.copy()

    store_daily = df.groupby(["date", "store_id"])["units_sold"].sum().reset_index()

    mean = store_daily["units_sold"].mean()
    std = store_daily["units_sold"].std()

    store_daily["z_score"] = (store_daily["units_sold"] - mean) / std

    anomalies = store_daily[np.abs(store_daily["z_score"]) > 3]

    return anomalies.sort_values("z_score", ascending=False)


# 3️. Price Simulation (Elasticity-Based)
def simulate_price_change(df, pct_change=0.05):

    if not -0.30 <= pct_change <= 0.30:
        raise ValueError("pct_change must be between -30% and +30%")

    elasticity = -1.2

    df = df.copy()

    original_revenue = df["revenue"].sum()

    df["new_price"] = df["price"] * (1 + pct_change)
    df["expected_units"] = df["units_sold"] * (1 + elasticity * pct_change)
    df["expected_units"] = np.maximum(df["expected_units"], 0)
    df["expected_revenue"] = df["new_price"] * df["expected_units"]

    new_revenue = df["expected_revenue"].sum()

    impact = {
        "original_revenue": round(original_revenue, 2),
        "projected_revenue": round(new_revenue, 2),
        "revenue_change_pct": round(
            ((new_revenue - original_revenue) / original_revenue) * 100, 2
        )
    }

    return impact


# 4. Promotion Simulation
def simulate_promo(df):

    promo_lift = 0.30

    df = df.copy()

    original_revenue = df["revenue"].sum()

    df["expected_units"] = df["units_sold"] * (1 + promo_lift)
    df["expected_revenue"] = df["expected_units"] * df["price"]

    new_revenue = df["expected_revenue"].sum()

    impact = {
        "original_revenue": round(original_revenue, 2),
        "projected_revenue": round(new_revenue, 2),
        "revenue_lift_pct": round(
            ((new_revenue - original_revenue) / original_revenue) * 100, 2
        )
    }

    return impact
