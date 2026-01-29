"""
FlowCast Insight Generator
Generates plain-English insights from financial metrics.
"""

from typing import List, Dict, Optional


class InsightGenerator:
    """Generates rule-based insights from financial data and metrics."""

    def __init__(self, data: dict, metrics: dict, forecast_data: dict = None):
        """
        Initialize the insight generator.

        Args:
            data: Parsed financial data
            metrics: Calculated metrics from MetricsCalculator
            forecast_data: Optional forecast data from Forecaster
        """
        self.data = data
        self.metrics = metrics
        self.forecast_data = forecast_data

    def generate_insights(self, max_insights: int = 5) -> List[dict]:
        """
        Generate a list of insights based on the data.

        Returns list of dicts with 'text', 'type' (positive/negative/neutral), 'priority'.
        """
        all_insights = []

        # Generate insights from various rules
        all_insights.extend(self._growth_insights())
        all_insights.extend(self._margin_insights())
        all_insights.extend(self._expense_insights())
        all_insights.extend(self._forecast_insights())

        # Sort by priority and return top N
        all_insights.sort(key=lambda x: x['priority'], reverse=True)
        return all_insights[:max_insights]

    def _growth_insights(self) -> List[dict]:
        """Generate insights about growth trends."""
        insights = []

        rev_growth = self.metrics.get('revenue_growth_rate', {})
        exp_growth = self.metrics.get('expense_growth_rate', {})

        rev_rate = rev_growth.get('value')
        exp_rate = exp_growth.get('value')

        # Check if expenses growing faster than revenue
        if rev_rate is not None and exp_rate is not None:
            if exp_rate > rev_rate + 2:  # Expenses growing significantly faster
                diff = exp_rate - rev_rate
                insights.append({
                    'text': f"Admin costs grew {diff:.1f}% faster than revenue - monitor cost control",
                    'type': 'negative',
                    'priority': 9,
                    'category': 'growth'
                })
            elif rev_rate > exp_rate + 2:  # Revenue growing faster
                diff = rev_rate - exp_rate
                insights.append({
                    'text': f"Revenue outpaced admin costs by {diff:.1f}% - good cost management",
                    'type': 'positive',
                    'priority': 7,
                    'category': 'growth'
                })

        # Revenue trend insight
        rev_trend = self.metrics.get('revenue_trend', {})
        if rev_trend.get('status') == 'green':
            insights.append({
                'text': "Revenue shows consistent growth trend",
                'type': 'positive',
                'priority': 6,
                'category': 'growth'
            })
        elif rev_trend.get('status') == 'red':
            insights.append({
                'text': "Revenue is declining - investigate causes and consider action",
                'type': 'negative',
                'priority': 10,
                'category': 'growth'
            })

        return insights

    def _margin_insights(self) -> List[dict]:
        """Generate insights about profit margins."""
        insights = []

        gross_margin = self.metrics.get('gross_margin', {})
        operating_margin = self.metrics.get('operating_margin', {})

        # Gross margin insights
        gm_value = gross_margin.get('value', 0)
        if gm_value >= 50:
            insights.append({
                'text': f"Strong gross margin of {gm_value:.1f}% indicates healthy pricing/costs",
                'type': 'positive',
                'priority': 6,
                'category': 'margin'
            })
        elif gm_value < 20:
            insights.append({
                'text': f"Gross margin of {gm_value:.1f}% is tight - review pricing or cost of sales",
                'type': 'negative',
                'priority': 8,
                'category': 'margin'
            })
        elif gm_value >= 30:
            insights.append({
                'text': f"Gross margin of {gm_value:.1f}% is healthy",
                'type': 'positive',
                'priority': 4,
                'category': 'margin'
            })

        # Operating margin insights
        om_value = operating_margin.get('value', 0)
        if om_value < 0:
            insights.append({
                'text': f"Operating at a loss ({om_value:.1f}% margin) - admin costs exceed gross profit",
                'type': 'negative',
                'priority': 10,
                'category': 'margin'
            })
        elif om_value < 5:
            insights.append({
                'text': f"Operating margin of {om_value:.1f}% is very thin - limited buffer for unexpected costs",
                'type': 'negative',
                'priority': 8,
                'category': 'margin'
            })
        elif om_value >= 20:
            insights.append({
                'text': f"Strong operating margin of {om_value:.1f}% provides good financial resilience",
                'type': 'positive',
                'priority': 6,
                'category': 'margin'
            })

        return insights

    def _expense_insights(self) -> List[dict]:
        """Generate insights about expenses."""
        insights = []

        largest_expense = self.metrics.get('largest_expense', {})
        burn_rate = self.metrics.get('monthly_burn_rate', {})

        # Expense concentration insight
        exp_pct = largest_expense.get('percentage', 0)
        exp_category = largest_expense.get('category', 'Unknown')

        if exp_pct > 70:
            insights.append({
                'text': f"'{exp_category}' dominates admin costs at {exp_pct:.0f}% - high concentration risk",
                'type': 'negative',
                'priority': 7,
                'category': 'expense'
            })
        elif exp_pct > 50:
            insights.append({
                'text': f"'{exp_category}' represents {exp_pct:.0f}% of admin costs",
                'type': 'neutral',
                'priority': 5,
                'category': 'expense'
            })

        # Monthly burn rate context
        burn_value = burn_rate.get('value', 0)
        total_revenue = self.metrics.get('total_revenue', {}).get('value', 0)

        if total_revenue > 0 and burn_value > 0:
            months_data = len(self.data.get('months', []))
            avg_monthly_revenue = total_revenue / months_data if months_data > 0 else 0

            if avg_monthly_revenue > 0:
                burn_ratio = (burn_value / avg_monthly_revenue) * 100
                if burn_ratio > 80:
                    insights.append({
                        'text': f"Admin costs consume {burn_ratio:.0f}% of average monthly revenue",
                        'type': 'negative',
                        'priority': 7,
                        'category': 'expense'
                    })

        return insights

    def _forecast_insights(self) -> List[dict]:
        """Generate insights from forecast data."""
        if not self.forecast_data:
            return []

        insights = []
        breakeven = self.forecast_data.get('breakeven_analysis', {})

        # Profitability crossover insight
        crossover_month = breakeven.get('crossover_month')
        crossover_type = breakeven.get('crossover_type')

        if crossover_month:
            if crossover_type == 'profit_to_loss':
                insights.append({
                    'text': f"At current trends, operating profit may turn negative by {crossover_month}",
                    'type': 'negative',
                    'priority': 9,
                    'category': 'forecast'
                })
            elif crossover_type == 'loss_to_profit':
                insights.append({
                    'text': f"At current trends, operating profit may turn positive by {crossover_month}",
                    'type': 'positive',
                    'priority': 8,
                    'category': 'forecast'
                })

        # Final forecast value insight
        final_value = breakeven.get('final_forecast_value')
        final_month = breakeven.get('final_forecast_month')

        if final_value is not None and final_month:
            if final_value > 0:
                insights.append({
                    'text': f"Projected operating profit of {final_value:,.0f} by {final_month}",
                    'type': 'positive',
                    'priority': 5,
                    'category': 'forecast'
                })
            elif final_value < 0:
                insights.append({
                    'text': f"Projected operating loss of {abs(final_value):,.0f} by {final_month}",
                    'type': 'negative',
                    'priority': 7,
                    'category': 'forecast'
                })

        # Revenue forecast reliability
        rev_forecast = self.forecast_data.get('revenue', {})
        r_squared = rev_forecast.get('r_squared', 0)

        if r_squared < 0.5:
            insights.append({
                'text': "Revenue trend is variable - forecast has higher uncertainty",
                'type': 'neutral',
                'priority': 3,
                'category': 'forecast'
            })
        elif r_squared > 0.9:
            insights.append({
                'text': "Revenue follows a consistent pattern - forecast is more reliable",
                'type': 'positive',
                'priority': 4,
                'category': 'forecast'
            })

        return insights

    def get_summary_text(self) -> str:
        """Generate a single paragraph summary of key insights."""
        insights = self.generate_insights(max_insights=3)

        if not insights:
            return "Insufficient data to generate insights."

        # Combine top insights into a summary
        summary_parts = [insight['text'] for insight in insights]
        return " ".join(summary_parts)
