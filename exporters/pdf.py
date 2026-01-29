"""
FlowCast PDF Exporter
Creates a beautiful single-page PDF report with metrics summary and insights.
"""

from io import BytesIO
from fpdf import FPDF
from typing import List, Dict, Optional

# Books & Balances Brand Colors (RGB)
BRAND_PRIMARY = (27, 79, 114)      # Deep navy
BRAND_SECONDARY = (20, 143, 119)   # Teal
BRAND_POSITIVE = (39, 174, 96)     # Green
BRAND_NEGATIVE = (231, 76, 60)     # Red
BRAND_TEXT = (44, 62, 80)          # Dark text
BRAND_LIGHT = (127, 140, 141)      # Light text


class FlowCastPDF(FPDF):
    """Custom PDF class for FlowCast reports with Books & Balances branding."""

    def __init__(self, currency: str = '£'):
        super().__init__()
        self.currency = currency
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        # Brand tag
        self.set_font('Helvetica', '', 8)
        self.set_text_color(*BRAND_SECONDARY)
        self.cell(0, 5, 'BOOKS & BALANCES', ln=True, align='C')

        # Main title
        self.set_font('Helvetica', 'B', 24)
        self.set_text_color(*BRAND_PRIMARY)
        self.cell(0, 12, 'FlowCast', ln=True, align='C')

        # Subtitle
        self.set_font('Helvetica', '', 10)
        self.set_text_color(*BRAND_LIGHT)
        self.cell(0, 6, 'Financial Health Report', ln=True, align='C')
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(*BRAND_LIGHT)
        self.cell(0, 10, f'Page {self.page_no()} | FlowCast by Books & Balances | booksandbalances.co.uk', align='C')

    def section_title(self, title: str):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(*BRAND_PRIMARY)
        self.cell(0, 10, title, ln=True)
        # Underline
        self.set_draw_color(*BRAND_SECONDARY)
        self.set_line_width(0.5)
        self.line(self.get_x(), self.get_y(), self.get_x() + 50, self.get_y())
        self.ln(5)

    def add_metric_row(self, label: str, value: str, status: str = 'neutral'):
        """Add a metric row with status indicator."""
        # Status colors
        status_colors = {
            'green': BRAND_POSITIVE,
            'yellow': (243, 156, 18),
            'red': BRAND_NEGATIVE,
            'neutral': BRAND_LIGHT
        }

        # Status indicator circle
        color = status_colors.get(status, status_colors['neutral'])
        self.set_fill_color(*color)
        y_center = self.get_y() + 3
        self.ellipse(self.get_x() + 2, y_center, 4, 4, style='F')
        self.set_x(self.get_x() + 12)

        # Label
        self.set_font('Helvetica', '', 10)
        self.set_text_color(*BRAND_TEXT)
        self.cell(55, 8, label)

        # Value
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(*color)
        self.cell(40, 8, value)
        self.ln()

    def add_insight(self, text: str, insight_type: str = 'neutral'):
        """Add an insight with color-coded styling."""
        # Background colors (lighter versions)
        bg_colors = {
            'positive': (232, 248, 245),
            'negative': (253, 237, 236),
            'neutral': (235, 245, 251)
        }

        border_colors = {
            'positive': BRAND_POSITIVE,
            'negative': BRAND_NEGATIVE,
            'neutral': BRAND_PRIMARY
        }

        bg = bg_colors.get(insight_type, bg_colors['neutral'])
        border = border_colors.get(insight_type, border_colors['neutral'])

        # Calculate dimensions
        self.set_font('Helvetica', '', 9)
        text_width = self.w - 35
        lines = self.multi_cell(text_width, 5, text, split_only=True)
        height = len(lines) * 5 + 8

        # Draw background
        self.set_fill_color(*bg)
        self.rect(15, self.get_y(), self.w - 30, height, style='F')

        # Draw left border
        self.set_fill_color(*border)
        self.rect(15, self.get_y(), 3, height, style='F')

        # Draw text
        self.set_xy(22, self.get_y() + 4)
        self.set_text_color(*BRAND_TEXT)
        self.multi_cell(text_width - 10, 5, text)
        self.ln(4)


def create_pdf_report(data: dict, metrics: dict, insights: List[dict],
                      forecast_data: dict = None, currency: str = '£') -> bytes:
    """
    Create a beautiful PDF report with Books & Balances branding.

    Args:
        data: Parsed financial data
        metrics: Calculated metrics dictionary
        insights: List of insight dictionaries
        forecast_data: Optional forecast data
        currency: Currency symbol

    Returns:
        PDF file as bytes
    """
    pdf = FlowCastPDF(currency=currency)
    pdf.add_page()

    # Company info
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(*BRAND_TEXT)
    company = data.get('company', 'Company')
    pdf.cell(0, 8, company, ln=True, align='C')

    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(*BRAND_LIGHT)
    period = data.get('period', '')
    pdf.cell(0, 6, period, ln=True, align='C')
    pdf.ln(10)

    # Financial Health Summary
    pdf.section_title('Financial Health Summary')

    # Key metrics with status indicators
    key_metrics = [
        ('Gross Margin', metrics.get('gross_margin', {})),
        ('Operating Margin', metrics.get('operating_margin', {})),
        ('Revenue Trend', metrics.get('revenue_trend', {})),
        ('Cost Control', metrics.get('cost_control', {})),
    ]

    for label, metric in key_metrics:
        value = metric.get('formatted', 'N/A')
        status = metric.get('status', 'neutral')
        pdf.add_metric_row(label, value, status)

    pdf.ln(8)

    # Key Figures
    pdf.section_title('Key Figures')

    total_revenue = metrics.get('total_revenue', {}).get('value', 0)
    total_profit = metrics.get('total_profit', {}).get('value', 0)
    burn_rate = metrics.get('monthly_burn_rate', {}).get('value', 0)
    largest_exp = metrics.get('largest_expense', {})

    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(*BRAND_TEXT)

    figures = [
        ('Total Revenue', f'{currency}{total_revenue:,.0f}'),
        ('Total Operating Profit', f'{currency}{total_profit:,.0f}'),
        ('Avg Monthly Burn Rate', f'{currency}{burn_rate:,.0f}'),
        ('Largest Expense', f"{largest_exp.get('category', 'N/A')} ({largest_exp.get('percentage', 0):.0f}%)"),
    ]

    for label, value in figures:
        pdf.cell(60, 7, label + ':')
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_text_color(*BRAND_PRIMARY)
        pdf.cell(0, 7, str(value), ln=True)
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(*BRAND_TEXT)

    pdf.ln(8)

    # Insights section
    if insights:
        pdf.section_title('Key Insights')

        for insight in insights[:5]:
            pdf.add_insight(insight['text'], insight['type'])

    pdf.ln(5)

    # Forecast summary
    if forecast_data:
        pdf.section_title('6-Month Forecast')

        breakeven = forecast_data.get('breakeven_analysis', {})

        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(*BRAND_TEXT)

        # Current status
        currently_profitable = breakeven.get('currently_profitable', False)
        status_text = 'Currently Profitable' if currently_profitable else 'Currently Operating at Loss'
        pdf.cell(0, 7, f'Status: {status_text}', ln=True)

        # Forecast months
        forecast_months = forecast_data.get('months', [])
        if forecast_months:
            pdf.cell(0, 7, f'Forecast Period: {forecast_months[0]} to {forecast_months[-1]}', ln=True)

        # Projected values
        if 'revenue' in forecast_data:
            final_rev = forecast_data['revenue']['values'][-1]
            pdf.cell(0, 7, f'Projected Revenue (End): {currency}{final_rev:,.0f}', ln=True)

        if 'operating_profit' in forecast_data:
            final_op = forecast_data['operating_profit']['values'][-1]
            pdf.cell(0, 7, f'Projected Operating Profit (End): {currency}{final_op:,.0f}', ln=True)

        # Crossover warning
        crossover = breakeven.get('crossover_month')
        crossover_type = breakeven.get('crossover_type')

        if crossover:
            pdf.ln(4)
            pdf.set_font('Helvetica', 'B', 10)
            if crossover_type == 'profit_to_loss':
                pdf.set_text_color(*BRAND_NEGATIVE)
                pdf.cell(0, 7, f'Warning: May turn unprofitable by {crossover}', ln=True)
            else:
                pdf.set_text_color(*BRAND_POSITIVE)
                pdf.cell(0, 7, f'Outlook: May turn profitable by {crossover}', ln=True)

    # Output to bytes
    output = BytesIO()
    pdf.output(output)
    output.seek(0)
    return output.getvalue()
