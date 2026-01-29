"""
FlowCast Metrics Calculator
Calculates key financial metrics and health indicators from parsed data.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional


class MetricsCalculator:
    """Calculates financial metrics and health indicators."""

    # Status thresholds
    GROSS_MARGIN_THRESHOLDS = {'green': 40, 'yellow': 20}  # >40% green, 20-40% yellow, <20% red
    OPERATING_MARGIN_THRESHOLDS = {'green': 15, 'yellow': 5}  # >15% green, 5-15% yellow, <5% red
    GROWTH_FLAT_THRESHOLD = 2  # +/- 2% considered flat

    def __init__(self, data: dict):
        self.data = data
        self.months = data['months']
        self.n_months = len(self.months)

    def calculate_all(self) -> dict:
        """Calculate all metrics and return as a dictionary."""
        return {
            'gross_margin': self.gross_margin_pct(),
            'operating_margin': self.operating_margin_pct(),
            'monthly_burn_rate': self.monthly_burn_rate(),
            'revenue_growth_rate': self.revenue_growth_rate(),
            'expense_growth_rate': self.expense_growth_rate(),
            'largest_expense': self.largest_expense(),
            'revenue_trend': self.revenue_trend(),
            'cost_control': self.cost_control(),
            'total_revenue': self.total_revenue(),
            'total_profit': self.total_operating_profit(),
        }

    def gross_margin_pct(self) -> dict:
        """Calculate gross margin percentage (Gross Profit / Revenue)."""
        total_revenue = sum(self.data['total_turnover'])
        total_gross_profit = sum(self.data['gross_profit'])

        if total_revenue == 0:
            return {'value': 0, 'formatted': '0%', 'status': 'red'}

        margin = (total_gross_profit / total_revenue) * 100
        status = self._get_margin_status(margin, self.GROSS_MARGIN_THRESHOLDS)

        return {
            'value': margin,
            'formatted': f'{margin:.1f}%',
            'status': status
        }

    def operating_margin_pct(self) -> dict:
        """Calculate operating margin percentage (Operating Profit / Revenue)."""
        total_revenue = sum(self.data['total_turnover'])
        total_operating_profit = sum(self.data['operating_profit'])

        if total_revenue == 0:
            return {'value': 0, 'formatted': '0%', 'status': 'red'}

        margin = (total_operating_profit / total_revenue) * 100
        status = self._get_margin_status(margin, self.OPERATING_MARGIN_THRESHOLDS)

        return {
            'value': margin,
            'formatted': f'{margin:.1f}%',
            'status': status
        }

    def monthly_burn_rate(self) -> dict:
        """Calculate average monthly administrative costs."""
        admin_costs = self.data['total_admin_costs']
        avg_burn = np.mean(admin_costs) if admin_costs else 0

        return {
            'value': avg_burn,
            'formatted': f'{avg_burn:,.0f}',
            'status': 'neutral'
        }

    def revenue_growth_rate(self) -> dict:
        """Calculate month-over-month revenue growth rate."""
        revenue = self.data['total_turnover']
        growth_rate, status = self._calculate_growth_rate(revenue)

        return {
            'value': growth_rate,
            'formatted': f'{growth_rate:+.1f}%' if growth_rate is not None else 'N/A',
            'status': status
        }

    def expense_growth_rate(self) -> dict:
        """Calculate month-over-month expense growth rate."""
        expenses = self.data['total_admin_costs']
        growth_rate, _ = self._calculate_growth_rate(expenses)

        # For expenses, lower is better, so invert the status logic
        if growth_rate is None:
            status = 'neutral'
        elif growth_rate < 0:
            status = 'green'  # Expenses decreasing is good
        elif growth_rate <= self.GROWTH_FLAT_THRESHOLD:
            status = 'yellow'
        else:
            status = 'red'  # Expenses increasing is concerning

        return {
            'value': growth_rate,
            'formatted': f'{growth_rate:+.1f}%' if growth_rate is not None else 'N/A',
            'status': status
        }

    def largest_expense(self) -> dict:
        """Find the largest admin cost category."""
        admin_breakdown = self.data.get('admin_breakdown', {})

        if not admin_breakdown:
            return {
                'category': 'N/A',
                'value': 0,
                'percentage': 0,
                'formatted': 'No data',
                'status': 'neutral'
            }

        # Get the first item (already sorted by total descending)
        top_category = list(admin_breakdown.keys())[0]
        top_value = admin_breakdown[top_category]['total']

        # Calculate percentage of total admin costs
        total_admin = sum(self.data['total_admin_costs'])
        percentage = (top_value / total_admin * 100) if total_admin > 0 else 0

        # Status: flag if one category dominates (>50%)
        status = 'yellow' if percentage > 50 else 'green'

        return {
            'category': top_category,
            'value': top_value,
            'percentage': percentage,
            'formatted': f'{top_category}: {percentage:.0f}%',
            'status': status
        }

    def revenue_trend(self) -> dict:
        """Determine if revenue is growing, flat, or declining."""
        revenue = self.data['total_turnover']

        if len(revenue) < 2:
            return {'value': 'N/A', 'status': 'neutral', 'formatted': 'Insufficient data'}

        # Use linear regression to determine trend
        x = np.arange(len(revenue))
        slope, _ = np.polyfit(x, revenue, 1)

        # Normalize slope to monthly percentage
        avg_revenue = np.mean(revenue)
        if avg_revenue == 0:
            return {'value': 'flat', 'status': 'yellow', 'formatted': 'Flat'}

        monthly_change_pct = (slope / avg_revenue) * 100

        if monthly_change_pct > self.GROWTH_FLAT_THRESHOLD:
            return {'value': 'growing', 'status': 'green', 'formatted': 'Growing'}
        elif monthly_change_pct < -self.GROWTH_FLAT_THRESHOLD:
            return {'value': 'declining', 'status': 'red', 'formatted': 'Declining'}
        else:
            return {'value': 'flat', 'status': 'yellow', 'formatted': 'Flat'}

    def cost_control(self) -> dict:
        """Compare expense growth to revenue growth."""
        rev_growth = self.revenue_growth_rate()['value']
        exp_growth = self.expense_growth_rate()['value']

        if rev_growth is None or exp_growth is None:
            return {
                'value': 'N/A',
                'status': 'neutral',
                'formatted': 'Insufficient data'
            }

        if exp_growth < rev_growth:
            return {
                'value': 'good',
                'status': 'green',
                'formatted': 'Costs < Revenue growth'
            }
        elif exp_growth > rev_growth + 5:  # Significant cost overrun
            return {
                'value': 'poor',
                'status': 'red',
                'formatted': 'Costs > Revenue growth'
            }
        else:
            return {
                'value': 'moderate',
                'status': 'yellow',
                'formatted': 'Costs tracking revenue'
            }

    def total_revenue(self) -> dict:
        """Get total revenue for the period."""
        total = sum(self.data['total_turnover'])
        return {
            'value': total,
            'formatted': f'{total:,.0f}',
            'status': 'neutral'
        }

    def total_operating_profit(self) -> dict:
        """Get total operating profit for the period."""
        total = sum(self.data['operating_profit'])
        status = 'green' if total > 0 else 'red'
        return {
            'value': total,
            'formatted': f'{total:,.0f}',
            'status': status
        }

    def _calculate_growth_rate(self, values: List[float]) -> Tuple[Optional[float], str]:
        """Calculate average month-over-month growth rate."""
        if len(values) < 2:
            return None, 'neutral'

        # Calculate compound monthly growth rate
        first_val = values[0] if values[0] != 0 else 0.01  # Avoid division by zero
        last_val = values[-1]
        n_periods = len(values) - 1

        if first_val <= 0:
            # Can't calculate meaningful growth rate from zero/negative start
            if last_val > 0:
                return None, 'green'  # Some improvement
            return None, 'neutral'

        # CMGR = (End/Start)^(1/n) - 1
        growth_rate = ((last_val / first_val) ** (1 / n_periods) - 1) * 100

        # Determine status
        if growth_rate > self.GROWTH_FLAT_THRESHOLD:
            status = 'green'
        elif growth_rate < -self.GROWTH_FLAT_THRESHOLD:
            status = 'red'
        else:
            status = 'yellow'

        return growth_rate, status

    @staticmethod
    def _get_margin_status(margin: float, thresholds: dict) -> str:
        """Determine status color based on margin thresholds."""
        if margin >= thresholds['green']:
            return 'green'
        elif margin >= thresholds['yellow']:
            return 'yellow'
        else:
            return 'red'

    def get_health_summary(self) -> dict:
        """Get a summary of overall financial health."""
        metrics = self.calculate_all()

        # Count statuses
        status_counts = {'green': 0, 'yellow': 0, 'red': 0, 'neutral': 0}
        key_metrics = ['gross_margin', 'operating_margin', 'revenue_trend', 'cost_control']

        for key in key_metrics:
            if key in metrics:
                status = metrics[key].get('status', 'neutral')
                status_counts[status] = status_counts.get(status, 0) + 1

        # Determine overall health
        if status_counts['red'] >= 2:
            overall = 'Needs Attention'
            overall_status = 'red'
        elif status_counts['green'] >= 3:
            overall = 'Healthy'
            overall_status = 'green'
        else:
            overall = 'Mixed'
            overall_status = 'yellow'

        return {
            'overall': overall,
            'overall_status': overall_status,
            'status_counts': status_counts,
            'metrics': metrics
        }
