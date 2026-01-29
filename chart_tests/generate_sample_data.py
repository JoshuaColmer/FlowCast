"""
Generate Sample Data for FlowCast Chart Variations
Creates synthetic financial data for testing professional chart styles
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Set random seed for reproducibility
np.random.seed(42)

# Output directory
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

def generate_monthly_financial_data():
    """
    Generate monthly financial data for Operating Profit chart (Chart 1)
    and Revenue & Profit Trends (Chart 3)
    """
    months = pd.date_range(start='2024-01-01', periods=12, freq='MS')

    # Base values with seasonal variation
    base_gross_profit = 85000
    base_admin_costs = 25000

    data = []
    for i, month in enumerate(months):
        # Add seasonal variation and growth trend
        seasonal_factor = 1 + 0.15 * np.sin(2 * np.pi * i / 12)
        growth_factor = 1 + 0.02 * i
        noise = np.random.normal(1, 0.05)

        gross_profit = base_gross_profit * seasonal_factor * growth_factor * noise
        admin_costs = base_admin_costs * (1 + 0.01 * i) * np.random.normal(1, 0.03)
        operating_profit = gross_profit - admin_costs

        # Revenue (for trends chart)
        revenue = gross_profit * 1.4 * np.random.normal(1, 0.02)

        data.append({
            'month': month.strftime('%Y-%m'),
            'month_name': month.strftime('%b'),
            'month_num': i + 1,
            'gross_profit': round(gross_profit, 2),
            'admin_costs': round(admin_costs, 2),
            'operating_profit': round(operating_profit, 2),
            'revenue': round(revenue, 2)
        })

    return pd.DataFrame(data)


def generate_admin_cost_breakdown():
    """
    Generate admin cost category breakdown for Donut/Pie chart (Chart 2)
    """
    categories = {
        'Salaries & Benefits': 45.2,
        'Office Rent': 18.5,
        'IT & Software': 12.3,
        'Professional Services': 8.7,
        'Marketing': 7.1,
        'Utilities': 4.2,
        'Other': 4.0
    }

    # Add some variation
    total = sum(categories.values())
    data = []
    for category, base_pct in categories.items():
        pct = base_pct + np.random.uniform(-0.5, 0.5)
        amount = round(25000 * 12 * (pct / 100), 2)  # Annual admin costs
        data.append({
            'category': category,
            'percentage': round(pct, 1),
            'amount': amount
        })

    # Normalize to 100%
    df = pd.DataFrame(data)
    df['percentage'] = round(df['percentage'] / df['percentage'].sum() * 100, 1)

    return df


def generate_forecast_data():
    """
    Generate historical + forecast data for Revenue & Profit Trends (Chart 3)
    """
    # Historical data (12 months)
    hist_months = pd.date_range(start='2024-01-01', periods=12, freq='MS')
    # Forecast data (6 months)
    forecast_months = pd.date_range(start='2025-01-01', periods=6, freq='MS')

    data = []

    # Historical data
    base_revenue = 120000
    base_gross_profit = 85000
    base_net_profit = 55000

    for i, month in enumerate(hist_months):
        growth = 1 + 0.025 * i
        seasonal = 1 + 0.12 * np.sin(2 * np.pi * i / 12)

        revenue = base_revenue * growth * seasonal * np.random.normal(1, 0.03)
        gross_profit = base_gross_profit * growth * seasonal * np.random.normal(1, 0.04)
        net_profit = base_net_profit * growth * seasonal * np.random.normal(1, 0.05)

        data.append({
            'date': month,
            'month_name': month.strftime('%b %Y'),
            'revenue': round(revenue, 2),
            'gross_profit': round(gross_profit, 2),
            'net_profit': round(net_profit, 2),
            'is_forecast': False,
            'revenue_lower': None,
            'revenue_upper': None,
            'gross_profit_lower': None,
            'gross_profit_upper': None,
            'net_profit_lower': None,
            'net_profit_upper': None
        })

    # Forecast data with confidence bands
    last_revenue = data[-1]['revenue']
    last_gross = data[-1]['gross_profit']
    last_net = data[-1]['net_profit']

    for i, month in enumerate(forecast_months):
        growth = 1 + 0.03 * (i + 1)
        uncertainty = 0.05 + 0.02 * i  # Increasing uncertainty

        revenue = last_revenue * growth
        gross_profit = last_gross * growth
        net_profit = last_net * growth

        data.append({
            'date': month,
            'month_name': month.strftime('%b %Y'),
            'revenue': round(revenue, 2),
            'gross_profit': round(gross_profit, 2),
            'net_profit': round(net_profit, 2),
            'is_forecast': True,
            'revenue_lower': round(revenue * (1 - uncertainty), 2),
            'revenue_upper': round(revenue * (1 + uncertainty), 2),
            'gross_profit_lower': round(gross_profit * (1 - uncertainty), 2),
            'gross_profit_upper': round(gross_profit * (1 + uncertainty), 2),
            'net_profit_lower': round(net_profit * (1 - uncertainty), 2),
            'net_profit_upper': round(net_profit * (1 + uncertainty), 2)
        })

    return pd.DataFrame(data)


def generate_cumulative_data():
    """
    Generate cumulative profit vs expenses data for Area chart (Chart 4)
    """
    months = pd.date_range(start='2024-01-01', periods=12, freq='MS')

    data = []
    cumulative_profit = 0
    cumulative_expenses = 0

    base_monthly_profit = 55000
    base_monthly_expenses = 65000

    for i, month in enumerate(months):
        # Monthly values with variation
        monthly_profit = base_monthly_profit * (1 + 0.03 * i) * np.random.normal(1, 0.08)
        monthly_expenses = base_monthly_expenses * (1 + 0.02 * i) * np.random.normal(1, 0.05)

        cumulative_profit += monthly_profit
        cumulative_expenses += monthly_expenses

        data.append({
            'date': month,
            'month_name': month.strftime('%b'),
            'month_num': i + 1,
            'monthly_profit': round(monthly_profit, 2),
            'monthly_expenses': round(monthly_expenses, 2),
            'cumulative_profit': round(cumulative_profit, 2),
            'cumulative_expenses': round(cumulative_expenses, 2),
            'net_position': round(cumulative_profit - cumulative_expenses, 2)
        })

    return pd.DataFrame(data)


def main():
    print("Generating FlowCast sample data...")

    # Generate all datasets
    monthly_data = generate_monthly_financial_data()
    admin_breakdown = generate_admin_cost_breakdown()
    forecast_data = generate_forecast_data()
    cumulative_data = generate_cumulative_data()

    # Save to CSV
    monthly_data.to_csv(os.path.join(OUTPUT_DIR, 'sample_data_monthly.csv'), index=False)
    admin_breakdown.to_csv(os.path.join(OUTPUT_DIR, 'sample_data_admin.csv'), index=False)
    forecast_data.to_csv(os.path.join(OUTPUT_DIR, 'sample_data_forecast.csv'), index=False)
    cumulative_data.to_csv(os.path.join(OUTPUT_DIR, 'sample_data_cumulative.csv'), index=False)

    print(f"\nGenerated files in {OUTPUT_DIR}:")
    print("  - sample_data_monthly.csv (Operating Profit chart)")
    print("  - sample_data_admin.csv (Cost Breakdown chart)")
    print("  - sample_data_forecast.csv (Revenue Trends chart)")
    print("  - sample_data_cumulative.csv (Cumulative Analysis chart)")

    # Print previews
    print("\n--- Monthly Financial Data Preview ---")
    print(monthly_data.head(3).to_string(index=False))

    print("\n--- Admin Cost Breakdown Preview ---")
    print(admin_breakdown.to_string(index=False))

    print("\n--- Forecast Data Preview ---")
    print(forecast_data[['month_name', 'revenue', 'is_forecast']].head(6).to_string(index=False))

    print("\n--- Cumulative Data Preview ---")
    print(cumulative_data[['month_name', 'cumulative_profit', 'cumulative_expenses']].head(4).to_string(index=False))

    print("\nSample data generation complete!")


if __name__ == '__main__':
    main()
