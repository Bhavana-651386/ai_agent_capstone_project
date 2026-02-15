import pandas as pd
import pytest

from src.tools import (
    analyze_trends,
    detect_anomalies,
    simulate_price_change,
    simulate_promo
)


# -----------------------------
# Sample Test Data
# -----------------------------
@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "date": pd.date_range("2024-01-01", periods=10),
        "store_id": [1]*10,
        "category": ["Beverages"]*10,
        "sku_id": [101]*10,
        "price": [10]*10,
        "units_sold": [100]*10,
        "revenue": [1000]*10
    })


# -----------------------------
# Trend Analysis Tests
# -----------------------------
def test_analyze_trends_returns_summary(sample_df):

    monthly, summary = analyze_trends(sample_df)

    assert not monthly.empty
    assert "total_revenue" in summary
    assert summary["total_revenue"] == 10000


# -----------------------------
# Anomaly Detection Tests
# -----------------------------
def test_detect_anomalies_runs(sample_df):

    anomalies = detect_anomalies(sample_df)

    assert isinstance(anomalies, pd.DataFrame)


# -----------------------------
# Price Simulation Tests
# -----------------------------
def test_price_simulation_valid(sample_df):

    impact = simulate_price_change(sample_df, pct_change=0.05)

    assert "original_revenue" in impact
    assert "projected_revenue" in impact
    assert "revenue_change_pct" in impact


def test_price_simulation_invalid(sample_df):

    with pytest.raises(ValueError):
        simulate_price_change(sample_df, pct_change=1.0)


# -----------------------------
# Promotion Simulation Tests
# -----------------------------
def test_promo_simulation(sample_df):

    impact = simulate_promo(sample_df)

    assert "original_revenue" in impact
    assert "projected_revenue" in impact
    assert "revenue_lift_pct" in impact
