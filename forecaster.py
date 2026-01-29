"""
FlowCast Forecaster Module
Generates 6-month financial projections using linear regression.
"""

import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import List, Dict, Optional, Tuple


class Forecaster:
    """Generates financial forecasts based on historical data."""

    def __init__(self, data: dict, horizon: int = 6):
        """
        Initialize the forecaster.

        Args:
            data: Parsed financial data dictionary
            horizon: Number of months to forecast (default 6)
        """
        self.data = data
        self.horizon = horizon
        self.months = data['months']
        self.n_historical = len(self.months)

    def generate_forecast(self) -> dict:
        """Generate complete forecast for all metrics."""
        forecast_months = self._generate_future_months()

        return {
            'months': forecast_months,
            'revenue': self._forecast_series(
                self.data['total_turnover'],
                'Revenue'
            ),
            'gross_profit': self._forecast_series(
                self.data['gross_profit'],
                'Gross Profit'
            ),
            'admin_costs': self._forecast_series(
                self.data['total_admin_costs'],
                'Admin Costs'
            ),
            'operating_profit': self._forecast_operating_profit(),
            'breakeven_analysis': self._analyze_breakeven(),
        }

    def _generate_future_months(self) -> List[str]:
        """Generate month labels for forecast period."""
        if not self.months:
            return []

        # Parse the last historical month
        last_month_str = self.months[-1]
        try:
            # Try different date formats
            for fmt in ['%b %Y', '%B %Y', '%m/%Y']:
                try:
                    last_date = datetime.strptime(last_month_str, fmt)
                    break
                except ValueError:
                    continue
            else:
                # Default: assume current date if parsing fails
                last_date = datetime.now()

            # Generate future months
            future_months = []
            for i in range(1, self.horizon + 1):
                future_date = last_date + relativedelta(months=i)
                future_months.append(future_date.strftime('%b %Y'))

            return future_months

        except Exception:
            # Fallback: generate generic month labels
            return [f'Month +{i}' for i in range(1, self.horizon + 1)]

    def _forecast_series(self, historical: List[float], name: str) -> dict:
        """
        Forecast a time series using linear regression.

        Returns dict with 'values', 'lower', 'upper' confidence bands.
        """
        if len(historical) < 2:
            # Not enough data for meaningful forecast
            return {
                'values': [0] * self.horizon,
                'lower': [0] * self.horizon,
                'upper': [0] * self.horizon,
                'slope': 0,
                'r_squared': 0,
            }

        # Fit linear regression
        x = np.arange(len(historical))
        y = np.array(historical)

        # Calculate regression coefficients
        slope, intercept = np.polyfit(x, y, 1)

        # Calculate R-squared
        y_pred = slope * x + intercept
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0

        # Calculate standard error of the estimate
        n = len(y)
        if n > 2:
            se = np.sqrt(ss_res / (n - 2))
        else:
            se = np.std(y)

        # Generate forecast values
        x_forecast = np.arange(len(historical), len(historical) + self.horizon)
        forecast_values = slope * x_forecast + intercept

        # Calculate confidence bands (approximately 95% CI)
        # Use 1.96 standard errors, scaled by distance from mean
        x_mean = np.mean(x)
        x_var = np.var(x) * n if np.var(x) > 0 else 1

        confidence_bands = []
        for xi in x_forecast:
            # Standard error increases with distance from data
            leverage = 1 + (1/n) + ((xi - x_mean) ** 2) / x_var
            margin = 1.96 * se * np.sqrt(leverage)
            confidence_bands.append(margin)

        confidence_bands = np.array(confidence_bands)

        # Ensure forecasts don't go negative for metrics that shouldn't
        forecast_values = np.maximum(forecast_values, 0)
        lower_bound = np.maximum(forecast_values - confidence_bands, 0)
        upper_bound = forecast_values + confidence_bands

        return {
            'values': forecast_values.tolist(),
            'lower': lower_bound.tolist(),
            'upper': upper_bound.tolist(),
            'slope': float(slope),
            'intercept': float(intercept),
            'r_squared': float(r_squared),
            'se': float(se),
        }

    def _forecast_operating_profit(self) -> dict:
        """
        Forecast operating profit based on gross profit and admin costs forecasts.

        Operating Profit = Gross Profit - Admin Costs
        """
        gp_forecast = self._forecast_series(self.data['gross_profit'], 'Gross Profit')
        admin_forecast = self._forecast_series(self.data['total_admin_costs'], 'Admin Costs')

        # Calculate operating profit forecast
        op_values = [
            gp - admin
            for gp, admin in zip(gp_forecast['values'], admin_forecast['values'])
        ]

        # Calculate confidence bands (combine uncertainties)
        # Using simple approach: sum the uncertainties
        op_lower = [
            gp_l - admin_u  # Worst case: low gross profit, high admin
            for gp_l, admin_u in zip(gp_forecast['lower'], admin_forecast['upper'])
        ]
        op_upper = [
            gp_u - admin_l  # Best case: high gross profit, low admin
            for gp_u, admin_l in zip(gp_forecast['upper'], admin_forecast['lower'])
        ]

        return {
            'values': op_values,
            'lower': op_lower,
            'upper': op_upper,
        }

    def _analyze_breakeven(self) -> dict:
        """
        Analyze when operating profit crosses zero.

        Returns information about breakeven point in forecast.
        """
        op_forecast = self._forecast_operating_profit()
        historical_op = self.data['operating_profit']

        # Combine historical and forecast
        all_op = historical_op + op_forecast['values']
        all_months = self.months + self._generate_future_months()

        # Check current status
        last_historical = historical_op[-1] if historical_op else 0
        currently_profitable = last_historical > 0

        # Find crossover point
        crossover_month = None
        crossover_type = None  # 'profit_to_loss' or 'loss_to_profit'

        for i in range(len(historical_op), len(all_op)):
            current = all_op[i]
            previous = all_op[i - 1]

            if previous >= 0 and current < 0:
                crossover_month = all_months[i]
                crossover_type = 'profit_to_loss'
                break
            elif previous < 0 and current >= 0:
                crossover_month = all_months[i]
                crossover_type = 'loss_to_profit'
                break

        # Calculate projected final operating profit
        final_forecast_op = op_forecast['values'][-1] if op_forecast['values'] else 0

        return {
            'currently_profitable': currently_profitable,
            'crossover_month': crossover_month,
            'crossover_type': crossover_type,
            'final_forecast_value': final_forecast_op,
            'final_forecast_month': all_months[-1] if all_months else None,
        }

    def get_forecast_summary(self) -> str:
        """Generate a human-readable forecast summary."""
        forecast = self.generate_forecast()
        breakeven = forecast['breakeven_analysis']

        summary_parts = []

        # Revenue trend
        rev = forecast['revenue']
        if rev['slope'] > 0:
            summary_parts.append(
                f"Revenue is projected to grow, reaching {forecast['revenue']['values'][-1]:,.0f} "
                f"by {forecast['months'][-1]}"
            )
        elif rev['slope'] < 0:
            summary_parts.append(
                f"Revenue is projected to decline to {forecast['revenue']['values'][-1]:,.0f} "
                f"by {forecast['months'][-1]}"
            )
        else:
            summary_parts.append("Revenue is projected to remain stable")

        # Profitability outlook
        if breakeven['crossover_month']:
            if breakeven['crossover_type'] == 'profit_to_loss':
                summary_parts.append(
                    f"Operating profit may turn negative by {breakeven['crossover_month']}"
                )
            else:
                summary_parts.append(
                    f"Operating profit may turn positive by {breakeven['crossover_month']}"
                )
        else:
            if breakeven['currently_profitable']:
                summary_parts.append("Projected to remain profitable through the forecast period")
            else:
                summary_parts.append("May remain unprofitable through the forecast period")

        return ". ".join(summary_parts) + "."
