"""
FlowCast Charts Module
Generates beautiful charts from parsed financial data.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.patches import FancyBboxPatch
from io import BytesIO

# Books & Balances Brand Color Scheme
COLORS = {
    # Primary palette
    'primary': '#1B4F72',       # Deep navy blue
    'primary_light': '#2E86AB', # Lighter blue
    'secondary': '#148F77',     # Teal green
    'accent': '#F39C12',        # Warm gold/amber

    # Semantic colors
    'positive': '#27AE60',      # Success green
    'negative': '#E74C3C',      # Alert red
    'warning': '#F39C12',       # Warning amber

    # Chart colors
    'revenue': '#1B4F72',       # Deep navy
    'gross_profit': '#148F77',  # Teal
    'operating_profit': '#27AE60', # Green
    'admin_costs': '#8E44AD',   # Purple
    'forecast': '#85929E',      # Muted gray-blue

    # Backgrounds
    'background': '#FAFBFC',
    'grid': '#E8E8E8',
}

# Default currency symbol
DEFAULT_CURRENCY = '£'


def set_chart_style():
    """Apply consistent chart styling."""
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['Segoe UI', 'Helvetica', 'Arial', 'sans-serif'],
        'font.size': 10,
        'axes.titlesize': 14,
        'axes.titleweight': 'bold',
        'axes.labelsize': 10,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.facecolor': COLORS['background'],
        'figure.facecolor': 'white',
        'grid.alpha': 0.3,
        'grid.color': COLORS['grid'],
    })


class ChartGenerator:
    """Generates beautiful charts from parsed data."""

    def __init__(self, data: dict, forecast_data: dict = None, currency: str = DEFAULT_CURRENCY):
        self.data = data
        self.months = data['months']
        self.forecast_data = forecast_data
        self.currency = currency
        set_chart_style()

    def _currency_formatter(self, x, p):
        """Format axis values with currency symbol."""
        if abs(x) >= 1_000_000:
            return f'{self.currency}{x/1_000_000:.1f}M'
        elif abs(x) >= 1_000:
            return f'{self.currency}{x/1_000:.0f}K'
        else:
            return f'{self.currency}{x:,.0f}'

    def _add_chart_branding(self, ax, fig):
        """Add subtle branding to chart."""
        fig.text(0.99, 0.01, 'Books & Balances', fontsize=8,
                color='#AAAAAA', ha='right', va='bottom', alpha=0.7,
                style='italic')

    def create_operating_profit_chart(self) -> plt.Figure:
        """Create operating profit bar chart with modern styling."""
        fig, ax = plt.subplots(figsize=(10, 6))

        x = np.arange(len(self.months))
        width = 0.25

        gross_profit = self.data['gross_profit']
        admin_costs = self.data['total_admin_costs']
        operating_profit = self.data['operating_profit']

        # Create bars with rounded edges effect through alpha gradient
        bars_op = ax.bar(x - width, operating_profit, width, label='Operating Profit',
               color=[COLORS['positive'] if v >= 0 else COLORS['negative'] for v in operating_profit],
               edgecolor='white', linewidth=0.5, zorder=3)
        bars_admin = ax.bar(x, admin_costs, width, label='Admin Costs',
                           color=COLORS['admin_costs'], edgecolor='white', linewidth=0.5, zorder=3)
        bars_gp = ax.bar(x + width, gross_profit, width, label='Gross Profit',
                        color=COLORS['gross_profit'], edgecolor='white', linewidth=0.5, zorder=3)

        # Styling
        ax.set_ylabel(f'Amount ({self.currency})', fontsize=11, fontweight='medium', color='#444')
        ax.set_title('Operating Profit Analysis', fontsize=16, fontweight='bold',
                    color=COLORS['primary'], pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(self.months, rotation=45, ha='right', fontsize=9)

        # Modern legend
        legend = ax.legend(loc='upper left', fontsize=9, frameon=True,
                          fancybox=True, shadow=False, framealpha=0.95)
        legend.get_frame().set_edgecolor('#E0E0E0')

        ax.axhline(y=0, color='#333', linestyle='-', linewidth=0.8, zorder=1)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(self._currency_formatter))
        ax.grid(axis='y', alpha=0.3, zorder=0)
        ax.set_axisbelow(True)

        # Add value labels on bars
        for bars in [bars_op, bars_gp]:
            for bar in bars:
                height = bar.get_height()
                if abs(height) > 0:
                    va = 'bottom' if height >= 0 else 'top'
                    offset = 3 if height >= 0 else -3
                    ax.annotate(f'{self.currency}{height:,.0f}',
                              xy=(bar.get_x() + bar.get_width() / 2, height),
                              xytext=(0, offset), textcoords="offset points",
                              ha='center', va=va, fontsize=7, color='#666')

        self._add_chart_branding(ax, fig)
        plt.tight_layout()
        return fig

    def create_admin_costs_pie(self) -> plt.Figure:
        """Create modern donut chart for admin costs."""
        fig, ax = plt.subplots(figsize=(10, 8))

        admin_data = self.data['admin_breakdown']
        if not admin_data:
            ax.text(0.5, 0.5, 'No admin cost data available', ha='center', va='center',
                   fontsize=14, color='#666')
            return fig

        labels = list(admin_data.keys())
        values = [item['total'] for item in admin_data.values()]

        # Modern color palette
        colors = [
            '#1B4F72', '#148F77', '#8E44AD', '#F39C12', '#E74C3C',
            '#3498DB', '#1ABC9C', '#9B59B6', '#E67E22', '#C0392B',
            '#2980B9', '#16A085', '#8E44AD', '#D35400', '#A93226',
        ]
        chart_colors = colors[:len(labels)]

        # Create donut chart
        wedges, texts, autotexts = ax.pie(
            values,
            labels=None,
            autopct=lambda pct: f'{pct:.1f}%' if pct > 5 else '',
            colors=chart_colors,
            startangle=90,
            pctdistance=0.75,
            wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2),
            textprops={'fontsize': 9, 'color': 'white', 'fontweight': 'bold'}
        )

        # Add center circle for donut effect
        centre_circle = plt.Circle((0, 0), 0.35, fc='white')
        ax.add_patch(centre_circle)

        # Add total in center
        total = sum(values)
        ax.text(0, 0.05, f'{self.currency}{total:,.0f}', ha='center', va='center',
               fontsize=20, fontweight='bold', color=COLORS['primary'])
        ax.text(0, -0.12, 'Total Admin Costs', ha='center', va='center',
               fontsize=10, color='#666')

        # Modern legend
        legend_labels = [f'{label}: {self.currency}{val:,.0f}' for label, val in zip(labels, values)]
        legend = ax.legend(wedges, legend_labels, title="Cost Categories",
                          loc="center left", bbox_to_anchor=(-0.35, 0.5),
                          fontsize=9, frameon=True, fancybox=True)
        legend.get_frame().set_edgecolor('#E0E0E0')
        legend.get_title().set_fontweight('bold')

        ax.set_title('Administrative Costs Breakdown', fontsize=16, fontweight='bold',
                    color=COLORS['primary'], pad=20)

        self._add_chart_branding(ax, fig)
        plt.tight_layout()
        return fig

    def create_revenue_profit_trend(self) -> plt.Figure:
        """Create revenue and profit trend chart with forecast overlay."""
        fig, ax = plt.subplots(figsize=(11, 6))

        # Historical data
        x_hist = np.arange(len(self.months))
        revenue = self.data['total_turnover']
        gross_profit = self.data['gross_profit']
        operating_profit = self.data['operating_profit']

        # Plot historical data with solid lines and markers
        ax.plot(x_hist, revenue, 'o-', label='Revenue', color=COLORS['revenue'],
                linewidth=2.5, markersize=8, markerfacecolor='white',
                markeredgewidth=2, zorder=5)
        ax.plot(x_hist, gross_profit, 's-', label='Gross Profit', color=COLORS['gross_profit'],
                linewidth=2.5, markersize=7, markerfacecolor='white',
                markeredgewidth=2, zorder=5)
        ax.plot(x_hist, operating_profit, '^-', label='Operating Profit',
                color=COLORS['operating_profit'], linewidth=2.5, markersize=7,
                markerfacecolor='white', markeredgewidth=2, zorder=5)

        # Fill area under revenue for visual impact
        ax.fill_between(x_hist, 0, revenue, alpha=0.1, color=COLORS['revenue'], zorder=1)

        all_months = list(self.months)

        # Plot forecast if available
        if self.forecast_data:
            forecast_months = self.forecast_data.get('months', [])
            n_forecast = len(forecast_months)
            x_forecast = np.arange(len(self.months), len(self.months) + n_forecast)
            all_months = self.months + forecast_months

            # Forecast revenue with confidence band
            if 'revenue' in self.forecast_data:
                fc_rev = self.forecast_data['revenue']
                # Connect historical to forecast
                ax.plot([x_hist[-1], x_forecast[0]], [revenue[-1], fc_rev['values'][0]],
                       '--', color=COLORS['revenue'], linewidth=2, alpha=0.6)
                ax.plot(x_forecast, fc_rev['values'], 'o--', color=COLORS['revenue'],
                        linewidth=2, markersize=6, alpha=0.6, markerfacecolor='white',
                        markeredgewidth=1.5)
                if 'lower' in fc_rev and 'upper' in fc_rev:
                    ax.fill_between(x_forecast, fc_rev['lower'], fc_rev['upper'],
                                   color=COLORS['revenue'], alpha=0.1)

            # Forecast gross profit
            if 'gross_profit' in self.forecast_data:
                fc_gp = self.forecast_data['gross_profit']
                ax.plot([x_hist[-1], x_forecast[0]], [gross_profit[-1], fc_gp['values'][0]],
                       '--', color=COLORS['gross_profit'], linewidth=2, alpha=0.6)
                ax.plot(x_forecast, fc_gp['values'], 's--', color=COLORS['gross_profit'],
                        linewidth=2, markersize=5, alpha=0.6, markerfacecolor='white',
                        markeredgewidth=1.5)
                if 'lower' in fc_gp and 'upper' in fc_gp:
                    ax.fill_between(x_forecast, fc_gp['lower'], fc_gp['upper'],
                                   color=COLORS['gross_profit'], alpha=0.1)

            # Forecast operating profit
            if 'operating_profit' in self.forecast_data:
                fc_op = self.forecast_data['operating_profit']
                ax.plot([x_hist[-1], x_forecast[0]], [operating_profit[-1], fc_op['values'][0]],
                       '--', color=COLORS['operating_profit'], linewidth=2, alpha=0.6)
                ax.plot(x_forecast, fc_op['values'], '^--', color=COLORS['operating_profit'],
                        linewidth=2, markersize=5, alpha=0.6, markerfacecolor='white',
                        markeredgewidth=1.5)
                if 'lower' in fc_op and 'upper' in fc_op:
                    ax.fill_between(x_forecast, fc_op['lower'], fc_op['upper'],
                                   color=COLORS['operating_profit'], alpha=0.1)

            # Add forecast zone indicator
            ax.axvspan(len(self.months) - 0.5, len(all_months) - 0.5,
                      alpha=0.05, color=COLORS['forecast'], zorder=0)
            ax.axvline(x=len(self.months) - 0.5, color=COLORS['forecast'],
                      linestyle=':', linewidth=2, alpha=0.7, zorder=2)

            # Forecast label
            mid_forecast = len(self.months) + n_forecast / 2 - 0.5
            ax.text(mid_forecast, ax.get_ylim()[1] * 0.95, 'FORECAST',
                   fontsize=10, color=COLORS['forecast'], ha='center',
                   fontweight='bold', alpha=0.8)

        # Styling
        ax.set_ylabel(f'Amount ({self.currency})', fontsize=11, fontweight='medium', color='#444')
        ax.set_title('Revenue & Profit Trends', fontsize=16, fontweight='bold',
                    color=COLORS['primary'], pad=20)
        ax.set_xticks(np.arange(len(all_months)))
        ax.set_xticklabels(all_months, rotation=45, ha='right', fontsize=9)

        legend = ax.legend(loc='upper left', fontsize=9, frameon=True,
                          fancybox=True, framealpha=0.95)
        legend.get_frame().set_edgecolor('#E0E0E0')

        ax.axhline(y=0, color='#333', linestyle='-', linewidth=0.8, zorder=1)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(self._currency_formatter))
        ax.grid(axis='y', alpha=0.3, zorder=0)
        ax.set_axisbelow(True)

        self._add_chart_branding(ax, fig)
        plt.tight_layout()
        return fig

    def create_profit_expenses_trend(self) -> plt.Figure:
        """Create cumulative profit vs expenses trend chart."""
        fig, ax = plt.subplots(figsize=(10, 6))

        x = np.arange(len(self.months))

        gross_c = self.data['gross_profit_cumulative']
        admin_c = self.data['admin_costs_cumulative']

        # Plot with gradient fill
        ax.plot(x, gross_c, 'o-', label='Gross Profit (Cumulative)',
                color=COLORS['positive'], linewidth=2.5, markersize=8,
                markerfacecolor='white', markeredgewidth=2, zorder=5)
        ax.fill_between(x, 0, gross_c, alpha=0.15, color=COLORS['positive'], zorder=1)

        ax.plot(x, admin_c, '^-', label='Admin Costs (Cumulative)',
                color=COLORS['negative'], linewidth=2.5, markersize=8,
                markerfacecolor='white', markeredgewidth=2, zorder=5)
        ax.fill_between(x, 0, admin_c, alpha=0.15, color=COLORS['negative'], zorder=1)

        # Add trend lines
        if len(x) > 1:
            z_gross = np.polyfit(x, gross_c, 1)
            p_gross = np.poly1d(z_gross)
            r2_gross = self._calculate_r2(gross_c, p_gross(x))
            ax.plot(x, p_gross(x), '--', color=COLORS['positive'], alpha=0.5,
                   linewidth=1.5, label=f'Gross Profit Trend (R² = {r2_gross:.2f})')

            z_admin = np.polyfit(x, admin_c, 1)
            p_admin = np.poly1d(z_admin)
            r2_admin = self._calculate_r2(admin_c, p_admin(x))
            ax.plot(x, p_admin(x), '--', color=COLORS['negative'], alpha=0.5,
                   linewidth=1.5, label=f'Admin Costs Trend (R² = {r2_admin:.2f})')

        # Styling
        ax.set_ylabel(f'Cumulative Amount ({self.currency})', fontsize=11,
                     fontweight='medium', color='#444')
        ax.set_title('Cumulative Profit vs Expenses', fontsize=16, fontweight='bold',
                    color=COLORS['primary'], pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(self.months, rotation=45, ha='right', fontsize=9)

        legend = ax.legend(loc='upper left', fontsize=8, frameon=True,
                          fancybox=True, framealpha=0.95)
        legend.get_frame().set_edgecolor('#E0E0E0')

        ax.yaxis.set_major_formatter(mticker.FuncFormatter(self._currency_formatter))
        ax.grid(axis='y', alpha=0.3, zorder=0)
        ax.set_axisbelow(True)

        self._add_chart_branding(ax, fig)
        plt.tight_layout()
        return fig

    @staticmethod
    def _calculate_r2(actual, predicted):
        actual = np.array(actual)
        predicted = np.array(predicted)
        ss_res = np.sum((actual - predicted) ** 2)
        ss_tot = np.sum((actual - np.mean(actual)) ** 2)
        return 1 - (ss_res / ss_tot) if ss_tot != 0 else 0


def fig_to_bytes(fig) -> bytes:
    """Convert matplotlib figure to bytes for download."""
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=450, bbox_inches='tight', facecolor='white')
    buf.seek(0)
    return buf.getvalue()
