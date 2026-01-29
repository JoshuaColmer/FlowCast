"""
FlowCast Professional Chart Variations - Python (STATE OF THE ART)
Premium publication-quality charts with numbered filenames for team review
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_DIR = Path(__file__).parent
OUTPUT_DIRS = {
    'operating_profit': BASE_DIR / '01_operating_profit',
    'cost_breakdown': BASE_DIR / '02_cost_breakdown',
    'revenue_trends': BASE_DIR / '03_revenue_trends',
    'cumulative': BASE_DIR / '04_cumulative_analysis'
}

DPI = 300
FIGSIZE_STANDARD = (14, 8)
FIGSIZE_WIDE = (16, 8)
FIGSIZE_DONUT = (12, 10)

# Premium Color Palettes
PALETTES = {
    'premium_blue': ['#0A2463', '#1E3A5F', '#3E5C76', '#748CAB', '#D4E4F7', '#F0F4F8'],
    'premium_teal': ['#014D4E', '#017374', '#019191', '#02BABA', '#7FDBDB', '#E6FAFA'],
    'premium_warm': ['#6B2737', '#A13D63', '#D4648A', '#E899AC', '#F5D0D8', '#FEF0F3'],
    'corporate': ['#1B365D', '#2E5090', '#5B7DB1', '#8FADD3', '#C3D7EE', '#E8F1F8'],
    'modern_gradient': ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe'],
    'nature_earth': ['#2D5016', '#4A7023', '#6B8E23', '#8DB255', '#B8D98A', '#E3F1D0'],
    'financial': ['#1B4F72', '#2874A6', '#5DADE2', '#85C1E9', '#AED6F1', '#D6EAF8'],
    'accent_gold': ['#B8860B', '#DAA520', '#F4C430', '#FFD700', '#FFEC8B', '#FFFACD'],
}

def format_currency(x, pos=None):
    """Format number as currency with K/M abbreviations"""
    if abs(x) >= 1_000_000:
        return f'£{x/1_000_000:.1f}M'
    elif abs(x) >= 1_000:
        return f'£{x/1_000:.0f}K'
    else:
        return f'£{x:.0f}'

def add_value_labels(ax, bars, fmt='£{:.0f}K', offset=0.02, fontsize=9, color='#333333'):
    """Add value labels above bars"""
    for bar in bars:
        height = bar.get_height()
        ax.annotate(fmt.format(height/1000),
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=fontsize, color=color, fontweight='medium')

# =============================================================================
# PREMIUM THEME FUNCTIONS
# =============================================================================

def apply_premium_style(fig, ax, title, subtitle=None, source=None):
    """Apply premium, modern styling"""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#E0E0E0')
    ax.spines['bottom'].set_color('#E0E0E0')
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)

    # Title block with proper spacing
    fig.text(0.06, 0.94, title, fontsize=22, fontweight='bold', color='#1a1a1a',
             transform=fig.transFigure, va='top')

    if subtitle:
        fig.text(0.06, 0.89, subtitle, fontsize=13, color='#666666',
                 transform=fig.transFigure, va='top')

    if source:
        fig.text(0.06, 0.02, source, fontsize=10, color='#999999', style='italic',
                 transform=fig.transFigure)

    ax.yaxis.grid(True, linestyle='-', alpha=0.2, color='#000000', linewidth=0.5)
    ax.xaxis.grid(False)
    ax.set_axisbelow(True)
    ax.tick_params(axis='both', labelsize=12, colors='#333333', length=0)

def apply_minimal_style(fig, ax, title, subtitle=None):
    """Apply ultra-clean minimal styling"""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.spines['bottom'].set_linewidth(1)

    fig.text(0.08, 0.93, title, fontsize=24, fontweight='bold', color='#111111',
             transform=fig.transFigure, va='top')

    if subtitle:
        fig.text(0.08, 0.87, subtitle, fontsize=12, color='#555555',
                 transform=fig.transFigure, va='top')

    ax.yaxis.grid(True, linestyle='-', alpha=0.15, color='#000000', linewidth=0.5)
    ax.xaxis.grid(False)
    ax.tick_params(axis='y', length=0, labelsize=12, colors='#444444')
    ax.tick_params(axis='x', length=0, labelsize=12, colors='#444444')

def apply_dark_accent_style(fig, ax, title, subtitle=None, accent_color='#E63946'):
    """Apply style with bold accent bar at top"""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#333333')
    ax.spines['bottom'].set_linewidth(1)

    # Accent bar at very top of figure
    fig.patches.append(mpatches.Rectangle((0, 0.97), 1, 0.03, transform=fig.transFigure,
                                           facecolor=accent_color, edgecolor='none', zorder=10))

    fig.text(0.06, 0.92, title, fontsize=22, fontweight='bold', color='#1a1a1a',
             transform=fig.transFigure, va='top')

    if subtitle:
        fig.text(0.06, 0.86, subtitle, fontsize=12, color='#555555',
                 transform=fig.transFigure, va='top')

    ax.yaxis.grid(True, linestyle='-', alpha=0.2, color='#000000', linewidth=0.5)
    ax.tick_params(axis='y', length=0, labelsize=12, colors='#444444')
    ax.tick_params(axis='x', length=0, labelsize=12, colors='#444444')

def apply_gradient_bg_style(fig, ax, title, subtitle=None):
    """Apply style with subtle gradient background effect"""
    ax.set_facecolor('#FAFBFC')
    fig.patch.set_facecolor('#FAFBFC')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#D0D0D0')
    ax.spines['bottom'].set_color('#D0D0D0')

    fig.text(0.06, 0.94, title, fontsize=22, fontweight='bold', color='#2C3E50',
             transform=fig.transFigure, va='top')

    if subtitle:
        fig.text(0.06, 0.88, subtitle, fontsize=12, color='#7F8C8D',
                 transform=fig.transFigure, va='top')

    ax.yaxis.grid(True, linestyle='--', alpha=0.4, color='#BDC3C7', linewidth=0.8)
    ax.tick_params(axis='both', labelsize=12, colors='#2C3E50', length=0)


# =============================================================================
# CHART 1: OPERATING PROFIT (Grouped Bar Chart)
# =============================================================================

def create_operating_profit_charts(data):
    """Generate premium Operating Profit chart variations"""
    output_dir = OUTPUT_DIRS['operating_profit']

    x = np.arange(len(data))
    width = 0.26
    chart_num = 1

    # --- VARIATION 01: Premium Corporate ---
    fig, ax = plt.subplots(figsize=FIGSIZE_STANDARD, facecolor='white')

    colors = ['#1B4F72', '#148F77', '#F4D03F']
    bars1 = ax.bar(x - width, data['gross_profit'], width, label='Gross Profit',
                   color=colors[0], edgecolor='white', linewidth=0.8)
    bars2 = ax.bar(x, data['admin_costs'], width, label='Admin Costs',
                   color=colors[1], edgecolor='white', linewidth=0.8)
    bars3 = ax.bar(x + width, data['operating_profit'], width, label='Operating Profit',
                   color=colors[2], edgecolor='white', linewidth=0.8)

    ax.set_xticks(x)
    ax.set_xticklabels(data['month_name'], fontsize=13)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))
    ax.set_ylim(0, data['gross_profit'].max() * 1.18)

    apply_premium_style(fig, ax, 'Monthly Operating Profit Analysis',
                        subtitle='Gross profit, administrative costs, and operating profit comparison │ FY 2024',
                        source='Source: FlowCast Financial Data')

    ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=False,
              edgecolor='#E0E0E0', fontsize=11, framealpha=0.95)

    plt.subplots_adjust(top=0.82, bottom=0.12, left=0.08, right=0.95)
    plt.savefig(output_dir / f'py_{chart_num:02d}_premium_corporate.png', dpi=DPI, facecolor='white')
    plt.close()
    chart_num += 1

    # --- VARIATION 02: Minimal Modern ---
    fig, ax = plt.subplots(figsize=FIGSIZE_STANDARD, facecolor='white')

    colors = ['#3498DB', '#95A5A6', '#E74C3C']
    bars1 = ax.bar(x - width, data['gross_profit'], width, label='Gross Profit', color=colors[0])
    bars2 = ax.bar(x, data['admin_costs'], width, label='Admin Costs', color=colors[1])
    bars3 = ax.bar(x + width, data['operating_profit'], width, label='Operating Profit', color=colors[2])

    ax.set_xticks(x)
    ax.set_xticklabels(data['month_name'], fontsize=13)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))
    ax.set_ylim(0, data['gross_profit'].max() * 1.18)

    apply_minimal_style(fig, ax, 'Operating Profit by Month',
                        subtitle='Financial performance metrics for fiscal year 2024')

    ax.legend(loc='upper right', frameon=False, fontsize=11)

    plt.subplots_adjust(top=0.80, bottom=0.12, left=0.08, right=0.95)
    plt.savefig(output_dir / f'py_{chart_num:02d}_minimal_modern.png', dpi=DPI, facecolor='white')
    plt.close()
    chart_num += 1

    # --- VARIATION 03: Bold Accent (Red) ---
    fig, ax = plt.subplots(figsize=FIGSIZE_STANDARD, facecolor='white')

    colors = ['#2C3E50', '#7F8C8D', '#E74C3C']
    bars1 = ax.bar(x - width, data['gross_profit'], width, label='Gross Profit', color=colors[0])
    bars2 = ax.bar(x, data['admin_costs'], width, label='Admin Costs', color=colors[1])
    bars3 = ax.bar(x + width, data['operating_profit'], width, label='Operating Profit', color=colors[2])

    ax.set_xticks(x)
    ax.set_xticklabels(data['month_name'], fontsize=13)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))
    ax.set_ylim(0, data['gross_profit'].max() * 1.18)

    apply_dark_accent_style(fig, ax, 'Operating Profit by Month',
                            subtitle='Key financial metrics comparison across the fiscal year',
                            accent_color='#E74C3C')

    ax.legend(loc='upper right', frameon=True, edgecolor='#E0E0E0', fontsize=11)

    plt.subplots_adjust(top=0.80, bottom=0.12, left=0.08, right=0.95)
    plt.savefig(output_dir / f'py_{chart_num:02d}_bold_accent_red.png', dpi=DPI, facecolor='white')
    plt.close()
    chart_num += 1

    # --- VARIATION 04: Soft Gradient Background ---
    fig, ax = plt.subplots(figsize=FIGSIZE_STANDARD, facecolor='#FAFBFC')

    colors = ['#5D6D7E', '#85929E', '#F5B041']
    bars1 = ax.bar(x - width, data['gross_profit'], width, label='Gross Profit', color=colors[0])
    bars2 = ax.bar(x, data['admin_costs'], width, label='Admin Costs', color=colors[1])
    bars3 = ax.bar(x + width, data['operating_profit'], width, label='Operating Profit', color=colors[2])

    ax.set_xticks(x)
    ax.set_xticklabels(data['month_name'], fontsize=13)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))
    ax.set_ylim(0, data['gross_profit'].max() * 1.18)

    apply_gradient_bg_style(fig, ax, 'Profit Breakdown by Month',
                            subtitle='Three key financial metrics compared across all months')

    ax.legend(loc='upper right', frameon=True, facecolor='white', edgecolor='#D0D0D0', fontsize=11)

    plt.subplots_adjust(top=0.80, bottom=0.12, left=0.08, right=0.95)
    plt.savefig(output_dir / f'py_{chart_num:02d}_soft_gradient.png', dpi=DPI, facecolor='#FAFBFC')
    plt.close()
    chart_num += 1

    # --- VARIATION 05: Data Labels on Bars ---
    fig, ax = plt.subplots(figsize=FIGSIZE_WIDE, facecolor='white')

    colors = ['#1ABC9C', '#3498DB', '#9B59B6']
    bars1 = ax.bar(x - width, data['gross_profit'], width, label='Gross Profit', color=colors[0])
    bars2 = ax.bar(x, data['admin_costs'], width, label='Admin Costs', color=colors[1])
    bars3 = ax.bar(x + width, data['operating_profit'], width, label='Operating Profit', color=colors[2])

    # Add data labels
    add_value_labels(ax, bars1, fontsize=8, color='#1ABC9C')
    add_value_labels(ax, bars3, fontsize=8, color='#9B59B6')

    ax.set_xticks(x)
    ax.set_xticklabels(data['month_name'], fontsize=12)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))
    ax.set_ylim(0, data['gross_profit'].max() * 1.25)

    apply_premium_style(fig, ax, 'Monthly Financial Performance',
                        subtitle='With annotated values for gross and operating profit',
                        source='Source: FlowCast Financial Data')

    ax.legend(loc='upper right', frameon=True, edgecolor='#E0E0E0', fontsize=11)

    plt.subplots_adjust(top=0.82, bottom=0.10, left=0.06, right=0.96)
    plt.savefig(output_dir / f'py_{chart_num:02d}_annotated_values.png', dpi=DPI, facecolor='white')
    plt.close()
    chart_num += 1

    # --- VARIATION 06: Viridis Accessible ---
    fig, ax = plt.subplots(figsize=FIGSIZE_STANDARD, facecolor='white')

    colors = ['#440154', '#21918c', '#fde725']
    bars1 = ax.bar(x - width, data['gross_profit'], width, label='Gross Profit', color=colors[0])
    bars2 = ax.bar(x, data['admin_costs'], width, label='Admin Costs', color=colors[1])
    bars3 = ax.bar(x + width, data['operating_profit'], width, label='Operating Profit', color=colors[2])

    ax.set_xticks(x)
    ax.set_xticklabels(data['month_name'], fontsize=13)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))
    ax.set_ylim(0, data['gross_profit'].max() * 1.18)

    apply_premium_style(fig, ax, 'Operating Profit Analysis',
                        subtitle='Colorblind-accessible visualization │ FY 2024')

    ax.legend(loc='upper right', frameon=True, edgecolor='#E0E0E0', fontsize=11)

    plt.subplots_adjust(top=0.82, bottom=0.12, left=0.08, right=0.95)
    plt.savefig(output_dir / f'py_{chart_num:02d}_viridis_accessible.png', dpi=DPI, facecolor='white')
    plt.close()
    chart_num += 1

    # --- VARIATION 07: Navy & Gold Executive ---
    fig, ax = plt.subplots(figsize=FIGSIZE_STANDARD, facecolor='white')

    colors = ['#0A2463', '#3E92CC', '#D4AF37']
    bars1 = ax.bar(x - width, data['gross_profit'], width, label='Gross Profit', color=colors[0])
    bars2 = ax.bar(x, data['admin_costs'], width, label='Admin Costs', color=colors[1])
    bars3 = ax.bar(x + width, data['operating_profit'], width, label='Operating Profit', color=colors[2])

    ax.set_xticks(x)
    ax.set_xticklabels(data['month_name'], fontsize=13)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))
    ax.set_ylim(0, data['gross_profit'].max() * 1.18)

    apply_dark_accent_style(fig, ax, 'Executive Financial Summary',
                            subtitle='Monthly operating profit performance overview',
                            accent_color='#D4AF37')

    ax.legend(loc='upper right', frameon=True, edgecolor='#E0E0E0', fontsize=11)

    plt.subplots_adjust(top=0.80, bottom=0.12, left=0.08, right=0.95)
    plt.savefig(output_dir / f'py_{chart_num:02d}_navy_gold_executive.png', dpi=DPI, facecolor='white')
    plt.close()
    chart_num += 1

    # --- VARIATION 08: Teal Professional ---
    fig, ax = plt.subplots(figsize=FIGSIZE_STANDARD, facecolor='white')

    colors = ['#014D4E', '#02BABA', '#FF6B6B']
    bars1 = ax.bar(x - width, data['gross_profit'], width, label='Gross Profit', color=colors[0])
    bars2 = ax.bar(x, data['admin_costs'], width, label='Admin Costs', color=colors[1])
    bars3 = ax.bar(x + width, data['operating_profit'], width, label='Operating Profit', color=colors[2])

    ax.set_xticks(x)
    ax.set_xticklabels(data['month_name'], fontsize=13)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))
    ax.set_ylim(0, data['gross_profit'].max() * 1.18)

    apply_minimal_style(fig, ax, 'Monthly Profit Analysis',
                        subtitle='Comprehensive view of profit metrics')

    ax.legend(loc='upper right', frameon=False, fontsize=11)

    plt.subplots_adjust(top=0.80, bottom=0.12, left=0.08, right=0.95)
    plt.savefig(output_dir / f'py_{chart_num:02d}_teal_professional.png', dpi=DPI, facecolor='white')
    plt.close()

    print(f"  Created 8 Operating Profit variations")


# =============================================================================
# CHART 2: COST BREAKDOWN (Donut/Pie Chart)
# =============================================================================

def add_pie_labels(ax, wedges, data, pct_distance=0.75, font_size=12, font_color='white',
                   show_amounts=False, min_pct_for_label=5, top_n_amounts=3):
    """Add percentage labels directly ON pie/donut slices"""
    for i, (wedge, pct) in enumerate(zip(wedges, data['percentage'])):
        if pct >= min_pct_for_label:  # Only show label if slice is large enough
            angle = (wedge.theta2 + wedge.theta1) / 2
            x = pct_distance * np.cos(np.radians(angle))
            y = pct_distance * np.sin(np.radians(angle))

            # Show percentage + amount for top N slices if requested
            label_text = f'{pct:.1f}%'
            if show_amounts and i < top_n_amounts and i < len(data):
                amt = data['amount'].iloc[i]
                label_text = f'{pct:.0f}%\n£{amt/1000:.0f}K'

            ax.text(x, y, label_text, ha='center', va='center',
                    fontsize=font_size, fontweight='bold', color=font_color,
                    linespacing=0.9)

def create_cost_breakdown_charts(data):
    """Generate premium Cost Breakdown chart variations"""
    output_dir = OUTPUT_DIRS['cost_breakdown']
    chart_num = 1

    # --- VARIATION 01: Premium Donut with Labels ON Slices ---
    fig, ax = plt.subplots(figsize=FIGSIZE_DONUT, facecolor='white')

    colors = ['#1B4F72', '#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B1F2B', '#95A5A6'][:len(data)]
    wedges, texts = ax.pie(data['percentage'], labels=None, startangle=90, colors=colors,
                           wedgeprops=dict(width=0.55, edgecolor='white', linewidth=3))

    # Add percentage labels ON the slices
    add_pie_labels(ax, wedges, data, pct_distance=0.72, font_size=13, font_color='white', min_pct_for_label=6)

    ax.text(0, 0.05, '£302K', ha='center', va='center', fontsize=32, fontweight='bold', color='#1a1a1a')
    ax.text(0, -0.15, 'Total Annual', ha='center', va='center', fontsize=14, color='#666666')

    legend_labels = [f"{cat}" for cat in data['category']]
    ax.legend(wedges, legend_labels, loc='center left', bbox_to_anchor=(1.05, 0.5),
              frameon=False, fontsize=12, labelspacing=1.2)

    fig.text(0.5, 0.95, 'Administrative Cost Breakdown', fontsize=22, fontweight='bold',
             ha='center', transform=fig.transFigure)
    fig.text(0.5, 0.90, 'Annual expense distribution by category', fontsize=13, color='#666666',
             ha='center', transform=fig.transFigure)

    plt.subplots_adjust(left=0.05, right=0.65, top=0.85, bottom=0.05)
    plt.savefig(output_dir / f'py_{chart_num:02d}_premium_donut.png', dpi=DPI, facecolor='white', bbox_inches='tight')
    plt.close()
    chart_num += 1

    # --- VARIATION 02: Tableau Colors with Labels ON Slices ---
    fig, ax = plt.subplots(figsize=(12, 12), facecolor='white')

    colors = ['#4e79a7', '#f28e2b', '#e15759', '#76b7b2', '#59a14f', '#edc948', '#b07aa1'][:len(data)]
    wedges, texts = ax.pie(data['percentage'], labels=None, startangle=90, colors=colors,
                           wedgeprops=dict(width=0.5, edgecolor='white', linewidth=3))

    # Add percentage labels ON the slices
    add_pie_labels(ax, wedges, data, pct_distance=0.75, font_size=14, font_color='white', min_pct_for_label=6)

    total = data['amount'].sum()
    ax.text(0, 0.05, f'£{total/1000:.0f}K', ha='center', va='center', fontsize=36, fontweight='bold', color='#333333')
    ax.text(0, -0.12, 'Total', ha='center', va='center', fontsize=14, color='#666666')

    legend_labels = [f"{cat}" for cat in data['category']]
    ax.legend(wedges, legend_labels, loc='upper center', bbox_to_anchor=(0.5, -0.02),
              ncol=3, frameon=False, fontsize=12, columnspacing=1.5)

    fig.text(0.5, 0.93, 'Administrative Expenses', fontsize=24, fontweight='bold',
             ha='center', transform=fig.transFigure)
    fig.text(0.5, 0.88, 'Annual Breakdown by Category', fontsize=14, color='#666666',
             ha='center', transform=fig.transFigure)

    plt.subplots_adjust(top=0.82, bottom=0.15)
    plt.savefig(output_dir / f'py_{chart_num:02d}_tableau_bottom_legend.png', dpi=DPI, facecolor='white')
    plt.close()
    chart_num += 1

    # --- VARIATION 03: Horizontal Bar Ranked ---
    fig, ax = plt.subplots(figsize=FIGSIZE_STANDARD, facecolor='white')

    data_sorted = data.sort_values('percentage', ascending=True)
    y_pos = np.arange(len(data_sorted))

    colors = plt.cm.Blues(np.linspace(0.3, 0.9, len(data_sorted)))[::-1]
    bars = ax.barh(y_pos, data_sorted['percentage'], color=colors, height=0.7, edgecolor='white', linewidth=1)

    for bar, pct in zip(bars, data_sorted['percentage']):
        ax.text(bar.get_width() + 0.8, bar.get_y() + bar.get_height()/2,
                f'{pct}%', va='center', fontsize=13, fontweight='bold', color='#333333')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(data_sorted['category'], fontsize=13)
    ax.set_xlim(0, max(data_sorted['percentage']) * 1.2)
    ax.invert_yaxis()

    apply_premium_style(fig, ax, 'Administrative Cost Categories',
                        subtitle='Percentage distribution of total admin expenses │ Ranked by size',
                        source='Source: FlowCast Financial Data')
    ax.set_xlabel('Percentage of Total (%)', fontsize=12, labelpad=10)

    plt.subplots_adjust(top=0.82, bottom=0.12, left=0.22, right=0.95)
    plt.savefig(output_dir / f'py_{chart_num:02d}_horizontal_bar_ranked.png', dpi=DPI, facecolor='white')
    plt.close()
    chart_num += 1

    # --- VARIATION 04: Accent Bar Horizontal ---
    fig, ax = plt.subplots(figsize=FIGSIZE_STANDARD, facecolor='white')

    data_sorted = data.sort_values('percentage', ascending=True)
    y_pos = np.arange(len(data_sorted))

    bars = ax.barh(y_pos, data_sorted['percentage'], color='#2E86AB', height=0.65)

    for bar, pct in zip(bars, data_sorted['percentage']):
        ax.text(bar.get_width() + 0.6, bar.get_y() + bar.get_height()/2,
                f'{pct}%', va='center', fontsize=12, fontweight='bold', color='#2E86AB')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(data_sorted['category'], fontsize=13)
    ax.set_xlim(0, max(data_sorted['percentage']) * 1.2)
    ax.invert_yaxis()

    apply_dark_accent_style(fig, ax, 'Cost Distribution Analysis',
                            subtitle='Administrative expenses by category',
                            accent_color='#E63946')
    ax.set_xlabel('Percentage (%)', fontsize=12, labelpad=10)

    plt.subplots_adjust(top=0.80, bottom=0.12, left=0.22, right=0.95)
    plt.savefig(output_dir / f'py_{chart_num:02d}_accent_horizontal.png', dpi=DPI, facecolor='white')
    plt.close()
    chart_num += 1

    # --- VARIATION 05: Vertical Bar with Gradient ---
    fig, ax = plt.subplots(figsize=FIGSIZE_STANDARD, facecolor='white')

    data_ranked = data.sort_values('percentage', ascending=False)
    x_pos = np.arange(len(data_ranked))

    colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(data_ranked)))
    bars = ax.bar(x_pos, data_ranked['percentage'], color=colors, width=0.7, edgecolor='white', linewidth=1)

    for bar, pct in zip(bars, data_ranked['percentage']):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8,
                f'{pct}%', ha='center', va='bottom', fontsize=12, fontweight='bold', color='#333333')

    ax.set_xticks(x_pos)
    # Wrap long labels
    labels = ['\n'.join(cat.split(' ')) if len(cat) > 12 else cat for cat in data_ranked['category']]
    ax.set_xticklabels(labels, fontsize=11, ha='center')
    ax.set_ylim(0, max(data_ranked['percentage']) * 1.18)

    apply_minimal_style(fig, ax, 'Cost Category Distribution',
                        subtitle='Ranked by percentage of total admin costs')
    ax.set_ylabel('Percentage (%)', fontsize=12, labelpad=10)

    plt.subplots_adjust(top=0.80, bottom=0.18, left=0.10, right=0.95)
    plt.savefig(output_dir / f'py_{chart_num:02d}_vertical_gradient.png', dpi=DPI, facecolor='white')
    plt.close()
    chart_num += 1

    # --- VARIATION 06: Viridis Donut Accessible with Labels ---
    fig, ax = plt.subplots(figsize=FIGSIZE_DONUT, facecolor='white')

    colors = plt.cm.viridis(np.linspace(0.1, 0.9, len(data)))
    wedges, texts = ax.pie(data['percentage'], labels=None, startangle=90, colors=colors,
                           wedgeprops=dict(width=0.55, edgecolor='white', linewidth=2))

    # Add percentage labels ON the slices
    add_pie_labels(ax, wedges, data, pct_distance=0.72, font_size=13, font_color='white', min_pct_for_label=6)

    ax.text(0, 0, 'FY2024', ha='center', va='center', fontsize=18, color='#666666', fontweight='medium')

    legend_labels = [f"{cat}" for cat in data['category']]
    ax.legend(wedges, legend_labels, loc='center left', bbox_to_anchor=(1.05, 0.5),
              frameon=False, fontsize=12, labelspacing=1.2)

    fig.text(0.5, 0.95, 'Cost Distribution by Category', fontsize=22, fontweight='bold',
             ha='center', transform=fig.transFigure)
    fig.text(0.5, 0.90, 'Colorblind-accessible visualization', fontsize=13, color='#666666',
             ha='center', transform=fig.transFigure)

    plt.subplots_adjust(left=0.05, right=0.60, top=0.85, bottom=0.05)
    plt.savefig(output_dir / f'py_{chart_num:02d}_viridis_accessible.png', dpi=DPI, facecolor='white', bbox_inches='tight')
    plt.close()
    chart_num += 1

    # --- VARIATION 07: Navy & Gold Executive Donut with Labels + Amounts ---
    fig, ax = plt.subplots(figsize=FIGSIZE_DONUT, facecolor='white')

    colors = ['#0A2463', '#1E3A5F', '#3E5C76', '#748CAB', '#D4AF37', '#B8860B', '#8B7355'][:len(data)]
    wedges, texts = ax.pie(data['percentage'], labels=None, startangle=90, colors=colors,
                           wedgeprops=dict(width=0.5, edgecolor='white', linewidth=3))

    # Add percentage + amount labels ON the top 3 slices
    add_pie_labels(ax, wedges, data, pct_distance=0.75, font_size=13, font_color='white',
                   min_pct_for_label=6, show_amounts=True, top_n_amounts=3)

    total = data['amount'].sum()
    ax.text(0, 0.05, f'£{total/1000:.0f}K', ha='center', va='center', fontsize=34, fontweight='bold', color='#0A2463')
    ax.text(0, -0.12, 'Total Budget', ha='center', va='center', fontsize=13, color='#666666')

    legend_labels = [f"{cat}" for cat in data['category']]
    ax.legend(wedges, legend_labels, loc='center left', bbox_to_anchor=(1.05, 0.5),
              frameon=False, fontsize=12, labelspacing=1.2)

    fig.text(0.5, 0.95, 'Executive Budget Overview', fontsize=22, fontweight='bold',
             ha='center', transform=fig.transFigure)
    fig.text(0.5, 0.90, 'Administrative cost allocation with key figures', fontsize=13, color='#666666',
             ha='center', transform=fig.transFigure)

    plt.subplots_adjust(left=0.05, right=0.60, top=0.85, bottom=0.05)
    plt.savefig(output_dir / f'py_{chart_num:02d}_navy_gold_executive.png', dpi=DPI, facecolor='white', bbox_inches='tight')
    plt.close()
    chart_num += 1

    # --- VARIATION 08: Minimalist Pie with Labels ---
    fig, ax = plt.subplots(figsize=(11, 11), facecolor='white')

    colors = ['#2C3E50', '#34495E', '#5D6D7E', '#85929E', '#ABB2B9', '#D5D8DC', '#EBEDEF'][:len(data)]
    wedges, texts = ax.pie(data['percentage'], labels=None, startangle=90, colors=colors,
                           wedgeprops=dict(edgecolor='white', linewidth=2))

    # Add percentage labels ON the slices (use dark color for lighter slices)
    for i, (wedge, pct) in enumerate(zip(wedges, data['percentage'])):
        if pct >= 6:
            angle = (wedge.theta2 + wedge.theta1) / 2
            x = 0.65 * np.cos(np.radians(angle))
            y = 0.65 * np.sin(np.radians(angle))
            # Use white for dark slices, dark for light slices
            txt_color = 'white' if i < 4 else '#333333'
            ax.text(x, y, f'{pct:.1f}%', ha='center', va='center',
                    fontsize=13, fontweight='bold', color=txt_color)

    legend_labels = [f"{cat}" for cat in data['category']]
    ax.legend(wedges, legend_labels, loc='upper center', bbox_to_anchor=(0.5, -0.02),
              ncol=2, frameon=False, fontsize=12, columnspacing=2)

    fig.text(0.5, 0.93, 'Administrative Cost Distribution', fontsize=22, fontweight='normal',
             ha='center', transform=fig.transFigure)

    plt.subplots_adjust(top=0.88, bottom=0.12)
    plt.savefig(output_dir / f'py_{chart_num:02d}_minimalist_pie.png', dpi=DPI, facecolor='white')
    plt.close()

    print(f"  Created 8 Cost Breakdown variations")


# =============================================================================
# CHART 3: REVENUE & PROFIT TRENDS (Multi-line + Forecast)
# =============================================================================

def create_revenue_trends_charts(data):
    """Generate premium Revenue Trends chart variations"""
    output_dir = OUTPUT_DIRS['revenue_trends']

    historical = data[~data['is_forecast']].copy()
    forecast = data[data['is_forecast']].copy()
    all_months = list(historical['month_name']) + list(forecast['month_name'])

    x_hist = range(len(historical))
    x_fore_full = range(len(historical) - 1, len(data))
    fore_with_last = pd.concat([historical.tail(1), forecast])

    chart_num = 1

    # --- VARIATION 01: Premium Corporate with Confidence Bands ---
    fig, ax = plt.subplots(figsize=FIGSIZE_WIDE, facecolor='white')

    colors = ['#1B4F72', '#148F77', '#F4D03F']

    ax.fill_between(range(len(historical), len(data)), forecast['revenue_lower'], forecast['revenue_upper'],
                    alpha=0.15, color=colors[0])
    ax.fill_between(range(len(historical), len(data)), forecast['gross_profit_lower'], forecast['gross_profit_upper'],
                    alpha=0.15, color=colors[1])
    ax.fill_between(range(len(historical), len(data)), forecast['net_profit_lower'], forecast['net_profit_upper'],
                    alpha=0.15, color=colors[2])

    ax.plot(x_hist, historical['revenue'], color=colors[0], linewidth=2.5, marker='o', markersize=6, label='Revenue')
    ax.plot(x_hist, historical['gross_profit'], color=colors[1], linewidth=2.5, marker='s', markersize=6, label='Gross Profit')
    ax.plot(x_hist, historical['net_profit'], color=colors[2], linewidth=2.5, marker='^', markersize=6, label='Net Profit')

    ax.plot(x_fore_full, fore_with_last['revenue'], color=colors[0], linewidth=2, linestyle='--', alpha=0.7)
    ax.plot(x_fore_full, fore_with_last['gross_profit'], color=colors[1], linewidth=2, linestyle='--', alpha=0.7)
    ax.plot(x_fore_full, fore_with_last['net_profit'], color=colors[2], linewidth=2, linestyle='--', alpha=0.7)

    ax.axvline(x=len(historical) - 0.5, color='#CCCCCC', linestyle='-', linewidth=1.5)
    ax.text(len(historical) + 0.3, ax.get_ylim()[1] * 0.97, 'FORECAST', fontsize=11, color='#888888',
            fontweight='bold', style='italic')

    ax.set_xticks(range(len(data)))
    ax.set_xticklabels(all_months, rotation=45, ha='right', fontsize=11)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))

    apply_premium_style(fig, ax, 'Revenue & Profit Trends with Forecast',
                        subtitle='Historical performance (solid) and 6-month projection (dashed) with 95% confidence intervals',
                        source='Source: FlowCast Financial Data')

    ax.legend(loc='upper left', frameon=True, fancybox=True, edgecolor='#E0E0E0', fontsize=11)

    plt.subplots_adjust(top=0.82, bottom=0.15, left=0.08, right=0.96)
    plt.savefig(output_dir / f'py_{chart_num:02d}_premium_forecast.png', dpi=DPI, facecolor='white')
    plt.close()
    chart_num += 1

    # --- VARIATION 02: Minimal Modern ---
    fig, ax = plt.subplots(figsize=FIGSIZE_WIDE, facecolor='white')

    colors = ['#3498DB', '#2ECC71', '#F39C12']

    ax.plot(x_hist, historical['revenue'], color=colors[0], linewidth=3, label='Revenue')
    ax.plot(x_hist, historical['gross_profit'], color=colors[1], linewidth=3, label='Gross Profit')
    ax.plot(x_hist, historical['net_profit'], color=colors[2], linewidth=3, label='Net Profit')

    ax.plot(x_fore_full, fore_with_last['revenue'], color=colors[0], linewidth=2, linestyle=':', alpha=0.6)
    ax.plot(x_fore_full, fore_with_last['gross_profit'], color=colors[1], linewidth=2, linestyle=':', alpha=0.6)
    ax.plot(x_fore_full, fore_with_last['net_profit'], color=colors[2], linewidth=2, linestyle=':', alpha=0.6)

    ax.axvspan(len(historical) - 0.5, len(data) - 0.5, alpha=0.05, color='#333333')

    ax.set_xticks(range(len(data)))
    ax.set_xticklabels(all_months, rotation=45, ha='right', fontsize=11)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))

    apply_minimal_style(fig, ax, 'Financial Performance Outlook',
                        subtitle='Actual results and projected growth trajectory')

    ax.legend(loc='upper left', frameon=False, fontsize=12)

    plt.subplots_adjust(top=0.80, bottom=0.15, left=0.08, right=0.96)
    plt.savefig(output_dir / f'py_{chart_num:02d}_minimal_modern.png', dpi=DPI, facecolor='white')
    plt.close()
    chart_num += 1

    # --- VARIATION 03: Bold Accent Style ---
    fig, ax = plt.subplots(figsize=FIGSIZE_WIDE, facecolor='white')

    colors = ['#E74C3C', '#3498DB', '#2C3E50']

    ax.fill_between(range(len(historical), len(data)), forecast['revenue_lower'], forecast['revenue_upper'],
                    alpha=0.12, color=colors[0])

    ax.plot(x_hist, historical['revenue'], color=colors[0], linewidth=3, label='Revenue')
    ax.plot(x_hist, historical['gross_profit'], color=colors[1], linewidth=3, label='Gross Profit')
    ax.plot(x_hist, historical['net_profit'], color=colors[2], linewidth=3, label='Net Profit')

    ax.plot(x_fore_full, fore_with_last['revenue'], color=colors[0], linewidth=2.5, linestyle='--', alpha=0.7)
    ax.plot(x_fore_full, fore_with_last['gross_profit'], color=colors[1], linewidth=2.5, linestyle='--', alpha=0.7)
    ax.plot(x_fore_full, fore_with_last['net_profit'], color=colors[2], linewidth=2.5, linestyle='--', alpha=0.7)

    ax.axvline(x=len(historical) - 0.5, color='#CCCCCC', linestyle='-', linewidth=1)

    ax.set_xticks(range(len(data)))
    ax.set_xticklabels(all_months, rotation=45, ha='right', fontsize=11)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))

    apply_dark_accent_style(fig, ax, 'Revenue Trends Analysis',
                            subtitle='Historical data with projected growth and confidence band',
                            accent_color='#E74C3C')

    ax.legend(loc='upper left', frameon=True, edgecolor='#E0E0E0', fontsize=11)

    plt.subplots_adjust(top=0.80, bottom=0.15, left=0.08, right=0.96)
    plt.savefig(output_dir / f'py_{chart_num:02d}_bold_accent.png', dpi=DPI, facecolor='white')
    plt.close()
    chart_num += 1

    # --- VARIATION 04: Soft Background ---
    fig, ax = plt.subplots(figsize=FIGSIZE_WIDE, facecolor='#FAFBFC')

    colors = ['#5D6D7E', '#48C9B0', '#F5B041']

    ax.axvspan(len(historical) - 0.5, len(data) - 0.5, alpha=0.08, color='#2C3E50')

    ax.fill_between(range(len(historical), len(data)), forecast['revenue_lower'], forecast['revenue_upper'],
                    alpha=0.2, color=colors[0])

    ax.plot(x_hist, historical['revenue'], color=colors[0], linewidth=2.5, marker='o', markersize=5, label='Revenue')
    ax.plot(x_hist, historical['gross_profit'], color=colors[1], linewidth=2.5, marker='s', markersize=5, label='Gross Profit')
    ax.plot(x_hist, historical['net_profit'], color=colors[2], linewidth=2.5, marker='^', markersize=5, label='Net Profit')

    ax.plot(x_fore_full, fore_with_last['revenue'], color=colors[0], linewidth=2, linestyle='--', alpha=0.6)
    ax.plot(x_fore_full, fore_with_last['gross_profit'], color=colors[1], linewidth=2, linestyle='--', alpha=0.6)
    ax.plot(x_fore_full, fore_with_last['net_profit'], color=colors[2], linewidth=2, linestyle='--', alpha=0.6)

    ax.set_xticks(range(len(data)))
    ax.set_xticklabels(all_months, rotation=45, ha='right', fontsize=11)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))

    apply_gradient_bg_style(fig, ax, 'Financial Trends & Forecast',
                            subtitle='12-month historical with 6-month projection')

    ax.legend(loc='upper left', frameon=True, facecolor='white', edgecolor='#D0D0D0', fontsize=11)

    plt.subplots_adjust(top=0.80, bottom=0.15, left=0.08, right=0.96)
    plt.savefig(output_dir / f'py_{chart_num:02d}_soft_background.png', dpi=DPI, facecolor='#FAFBFC')
    plt.close()
    chart_num += 1

    # --- VARIATION 05: Viridis Accessible ---
    fig, ax = plt.subplots(figsize=FIGSIZE_WIDE, facecolor='white')

    colors = ['#440154', '#21918c', '#fde725']

    ax.fill_between(range(len(historical), len(data)), forecast['revenue_lower'], forecast['revenue_upper'],
                    alpha=0.2, color=colors[0])
    ax.fill_between(range(len(historical), len(data)), forecast['net_profit_lower'], forecast['net_profit_upper'],
                    alpha=0.2, color=colors[2])

    ax.plot(x_hist, historical['revenue'], color=colors[0], linewidth=2.5, marker='o', markersize=6, label='Revenue')
    ax.plot(x_hist, historical['gross_profit'], color=colors[1], linewidth=2.5, marker='s', markersize=6, label='Gross Profit')
    ax.plot(x_hist, historical['net_profit'], color=colors[2], linewidth=2.5, marker='^', markersize=6, label='Net Profit')

    ax.plot(x_fore_full, fore_with_last['revenue'], color=colors[0], linewidth=2, linestyle='--', alpha=0.6)
    ax.plot(x_fore_full, fore_with_last['gross_profit'], color=colors[1], linewidth=2, linestyle='--', alpha=0.6)
    ax.plot(x_fore_full, fore_with_last['net_profit'], color=colors[2], linewidth=2, linestyle='--', alpha=0.6)

    ax.axvline(x=len(historical) - 0.5, color='#999999', linestyle=':', linewidth=1.5)

    ax.set_xticks(range(len(data)))
    ax.set_xticklabels(all_months, rotation=45, ha='right', fontsize=11)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))

    apply_premium_style(fig, ax, 'Financial Performance Trends',
                        subtitle='Colorblind-accessible visualization with confidence intervals')

    ax.legend(loc='upper left', frameon=True, edgecolor='#E0E0E0', fontsize=11)

    plt.subplots_adjust(top=0.82, bottom=0.15, left=0.08, right=0.96)
    plt.savefig(output_dir / f'py_{chart_num:02d}_viridis_accessible.png', dpi=DPI, facecolor='white')
    plt.close()
    chart_num += 1

    # --- VARIATION 06: Navy & Gold Executive ---
    fig, ax = plt.subplots(figsize=FIGSIZE_WIDE, facecolor='white')

    colors = ['#0A2463', '#3E92CC', '#D4AF37']

    ax.fill_between(range(len(historical), len(data)), forecast['revenue_lower'], forecast['revenue_upper'],
                    alpha=0.12, color=colors[0])

    ax.plot(x_hist, historical['revenue'], color=colors[0], linewidth=3, marker='o', markersize=6, label='Revenue')
    ax.plot(x_hist, historical['gross_profit'], color=colors[1], linewidth=3, marker='s', markersize=6, label='Gross Profit')
    ax.plot(x_hist, historical['net_profit'], color=colors[2], linewidth=3, marker='^', markersize=6, label='Net Profit')

    ax.plot(x_fore_full, fore_with_last['revenue'], color=colors[0], linewidth=2, linestyle='--', alpha=0.7)
    ax.plot(x_fore_full, fore_with_last['gross_profit'], color=colors[1], linewidth=2, linestyle='--', alpha=0.7)
    ax.plot(x_fore_full, fore_with_last['net_profit'], color=colors[2], linewidth=2, linestyle='--', alpha=0.7)

    ax.axvline(x=len(historical) - 0.5, color='#D4AF37', linestyle='-', linewidth=2, alpha=0.5)
    ax.text(len(historical) + 0.3, ax.get_ylim()[1] * 0.95, 'FORECAST', fontsize=10, color='#D4AF37', fontweight='bold')

    ax.set_xticks(range(len(data)))
    ax.set_xticklabels(all_months, rotation=45, ha='right', fontsize=11)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))

    apply_dark_accent_style(fig, ax, 'Executive Revenue Outlook',
                            subtitle='Strategic financial projections with confidence bounds',
                            accent_color='#D4AF37')

    ax.legend(loc='upper left', frameon=True, edgecolor='#E0E0E0', fontsize=11)

    plt.subplots_adjust(top=0.80, bottom=0.15, left=0.08, right=0.96)
    plt.savefig(output_dir / f'py_{chart_num:02d}_navy_gold_executive.png', dpi=DPI, facecolor='white')
    plt.close()

    print(f"  Created 6 Revenue Trends variations")


# =============================================================================
# CHART 4: CUMULATIVE ANALYSIS (Area + Trend)
# =============================================================================

def create_cumulative_charts(data):
    """Generate premium Cumulative Analysis chart variations"""
    output_dir = OUTPUT_DIRS['cumulative']

    from scipy import stats

    x = np.arange(len(data))
    slope_profit, intercept_profit, _, _, _ = stats.linregress(x, data['cumulative_profit'])
    slope_expenses, intercept_expenses, _, _, _ = stats.linregress(x, data['cumulative_expenses'])
    trend_profit = slope_profit * x + intercept_profit
    trend_expenses = slope_expenses * x + intercept_expenses

    chart_num = 1

    # --- VARIATION 01: Premium Corporate Area ---
    fig, ax = plt.subplots(figsize=FIGSIZE_STANDARD, facecolor='white')

    colors = ['#148F77', '#1B4F72']

    ax.fill_between(x, 0, data['cumulative_profit'], alpha=0.35, color=colors[0], label='Cumulative Profit')
    ax.fill_between(x, 0, data['cumulative_expenses'], alpha=0.25, color=colors[1], label='Cumulative Expenses')

    ax.plot(x, data['cumulative_profit'], color=colors[0], linewidth=2.5)
    ax.plot(x, data['cumulative_expenses'], color=colors[1], linewidth=2.5)
    ax.plot(x, trend_profit, color=colors[0], linewidth=1.5, linestyle='--', alpha=0.7)
    ax.plot(x, trend_expenses, color=colors[1], linewidth=1.5, linestyle='--', alpha=0.7)

    ax.set_xticks(x)
    ax.set_xticklabels(data['month_name'], fontsize=12)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))

    apply_premium_style(fig, ax, 'Cumulative Financial Performance',
                        subtitle='Year-to-date profit vs expenses with linear trend analysis (dashed)',
                        source='Source: FlowCast Financial Data')

    ax.legend(loc='upper left', frameon=True, edgecolor='#E0E0E0', fontsize=11)

    plt.subplots_adjust(top=0.82, bottom=0.12, left=0.10, right=0.95)
    plt.savefig(output_dir / f'py_{chart_num:02d}_premium_area.png', dpi=DPI, facecolor='white')
    plt.close()
    chart_num += 1

    # --- VARIATION 02: Minimal Modern ---
    fig, ax = plt.subplots(figsize=FIGSIZE_STANDARD, facecolor='white')

    colors = ['#2ECC71', '#E74C3C']

    ax.fill_between(x, 0, data['cumulative_profit'], alpha=0.3, color=colors[0])
    ax.fill_between(x, 0, data['cumulative_expenses'], alpha=0.2, color=colors[1])

    ax.plot(x, data['cumulative_profit'], color=colors[0], linewidth=3, label='Profit')
    ax.plot(x, data['cumulative_expenses'], color=colors[1], linewidth=3, label='Expenses')
    ax.plot(x, trend_profit, color='#333333', linewidth=1.5, linestyle=':', alpha=0.6)

    ax.set_xticks(x)
    ax.set_xticklabels(data['month_name'], fontsize=12)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))

    apply_minimal_style(fig, ax, 'Year-to-Date Financial Position',
                        subtitle='Cumulative profit and expenses with trend')

    ax.legend(loc='upper left', frameon=False, fontsize=12)

    plt.subplots_adjust(top=0.80, bottom=0.12, left=0.10, right=0.95)
    plt.savefig(output_dir / f'py_{chart_num:02d}_minimal_modern.png', dpi=DPI, facecolor='white')
    plt.close()
    chart_num += 1

    # --- VARIATION 03: Bold Accent ---
    fig, ax = plt.subplots(figsize=FIGSIZE_STANDARD, facecolor='white')

    colors = ['#3498DB', '#E74C3C']

    ax.fill_between(x, 0, data['cumulative_profit'], alpha=0.4, color=colors[0])
    ax.fill_between(x, 0, data['cumulative_expenses'], alpha=0.25, color=colors[1])

    ax.plot(x, data['cumulative_profit'], color=colors[0], linewidth=2.5, label='Profit')
    ax.plot(x, data['cumulative_expenses'], color=colors[1], linewidth=2.5, label='Expenses')
    ax.plot(x, trend_profit, color='#2C3E50', linewidth=1.5, linestyle=':', label='Trend')

    ax.set_xticks(x)
    ax.set_xticklabels(data['month_name'], fontsize=12)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))

    apply_dark_accent_style(fig, ax, 'Cumulative Financial Analysis',
                            subtitle='Year-to-date performance with trend projection',
                            accent_color='#E74C3C')

    ax.legend(loc='upper left', frameon=True, edgecolor='#E0E0E0', fontsize=11)

    plt.subplots_adjust(top=0.80, bottom=0.12, left=0.10, right=0.95)
    plt.savefig(output_dir / f'py_{chart_num:02d}_bold_accent.png', dpi=DPI, facecolor='white')
    plt.close()
    chart_num += 1

    # --- VARIATION 04: Net Position Bars ---
    fig, ax = plt.subplots(figsize=FIGSIZE_STANDARD, facecolor='white')

    net = data['cumulative_profit'] - data['cumulative_expenses']
    colors_bars = ['#27AE60' if v >= 0 else '#E74C3C' for v in net]

    ax.bar(x, net, color=colors_bars, alpha=0.8, edgecolor='white', linewidth=1)
    ax.axhline(y=0, color='#333333', linewidth=1.5)

    slope_net, intercept_net, _, _, _ = stats.linregress(x, net)
    trend_net = slope_net * x + intercept_net
    ax.plot(x, trend_net, color='#333333', linewidth=2, linestyle='--', label='Trend')

    ax.set_xticks(x)
    ax.set_xticklabels(data['month_name'], fontsize=12)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))

    apply_premium_style(fig, ax, 'Net Financial Position',
                        subtitle='Monthly cumulative profit minus expenses │ Green = surplus, Red = deficit',
                        source='Source: FlowCast Financial Data')

    ax.legend(loc='upper left', frameon=True, edgecolor='#E0E0E0', fontsize=11)

    plt.subplots_adjust(top=0.82, bottom=0.12, left=0.10, right=0.95)
    plt.savefig(output_dir / f'py_{chart_num:02d}_net_position_bars.png', dpi=DPI, facecolor='white')
    plt.close()
    chart_num += 1

    # --- VARIATION 05: Soft Background ---
    fig, ax = plt.subplots(figsize=FIGSIZE_STANDARD, facecolor='#FAFBFC')

    colors = ['#48C9B0', '#5D6D7E']

    ax.fill_between(x, 0, data['cumulative_profit'], alpha=0.4, color=colors[0])
    ax.fill_between(x, 0, data['cumulative_expenses'], alpha=0.3, color=colors[1])

    ax.plot(x, data['cumulative_profit'], color=colors[0], linewidth=3, label='Profit')
    ax.plot(x, data['cumulative_expenses'], color=colors[1], linewidth=3, label='Expenses')
    ax.plot(x, trend_profit, color='#2C3E50', linewidth=1.5, linestyle='--', alpha=0.7)

    ax.set_xticks(x)
    ax.set_xticklabels(data['month_name'], fontsize=12)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))

    apply_gradient_bg_style(fig, ax, 'Running Total Analysis',
                            subtitle='Cumulative financial metrics throughout the fiscal year')

    ax.legend(loc='upper left', frameon=True, facecolor='white', edgecolor='#D0D0D0', fontsize=11)

    plt.subplots_adjust(top=0.80, bottom=0.12, left=0.10, right=0.95)
    plt.savefig(output_dir / f'py_{chart_num:02d}_soft_background.png', dpi=DPI, facecolor='#FAFBFC')
    plt.close()
    chart_num += 1

    # --- VARIATION 06: Navy & Gold Executive ---
    fig, ax = plt.subplots(figsize=FIGSIZE_STANDARD, facecolor='white')

    colors = ['#3E92CC', '#0A2463']

    ax.fill_between(x, 0, data['cumulative_profit'], alpha=0.35, color=colors[0])
    ax.fill_between(x, 0, data['cumulative_expenses'], alpha=0.25, color=colors[1])

    ax.plot(x, data['cumulative_profit'], color=colors[0], linewidth=3, marker='o', markersize=5, label='Profit')
    ax.plot(x, data['cumulative_expenses'], color=colors[1], linewidth=3, marker='s', markersize=5, label='Expenses')
    ax.plot(x, trend_profit, color='#D4AF37', linewidth=2, linestyle='--', label='Profit Trend')

    ax.set_xticks(x)
    ax.set_xticklabels(data['month_name'], fontsize=12)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))

    apply_dark_accent_style(fig, ax, 'Executive Cumulative Summary',
                            subtitle='Year-to-date financial performance with trend analysis',
                            accent_color='#D4AF37')

    ax.legend(loc='upper left', frameon=True, edgecolor='#E0E0E0', fontsize=11)

    plt.subplots_adjust(top=0.80, bottom=0.12, left=0.10, right=0.95)
    plt.savefig(output_dir / f'py_{chart_num:02d}_navy_gold_executive.png', dpi=DPI, facecolor='white')
    plt.close()
    chart_num += 1

    # --- VARIATION 07: Dual Axis with Monthly ---
    fig, ax1 = plt.subplots(figsize=FIGSIZE_STANDARD, facecolor='white')

    colors = ['#1ABC9C', '#3498DB']

    ax1.fill_between(x, 0, data['cumulative_profit'], alpha=0.2, color=colors[0])
    ax1.plot(x, data['cumulative_profit'], color=colors[0], linewidth=2.5, label='Cum. Profit')
    ax1.plot(x, data['cumulative_expenses'], color=colors[1], linewidth=2.5, label='Cum. Expenses')

    ax1.set_xticks(x)
    ax1.set_xticklabels(data['month_name'], fontsize=12)
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))
    ax1.set_ylabel('Cumulative Amount', fontsize=12, color='#333333')

    ax2 = ax1.twinx()
    width = 0.35
    ax2.bar(x - width/2, data['monthly_profit'], width, alpha=0.4, color=colors[0], label='Monthly Profit')
    ax2.bar(x + width/2, data['monthly_expenses'], width, alpha=0.4, color=colors[1], label='Monthly Expenses')
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))
    ax2.set_ylabel('Monthly Amount', fontsize=12, color='#333333')

    apply_premium_style(fig, ax1, 'Cumulative vs Monthly Analysis',
                        subtitle='Lines show YTD cumulative totals │ Bars show monthly values')

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', frameon=True, edgecolor='#E0E0E0', fontsize=10)

    plt.subplots_adjust(top=0.82, bottom=0.12, left=0.10, right=0.90)
    plt.savefig(output_dir / f'py_{chart_num:02d}_dual_axis_monthly.png', dpi=DPI, facecolor='white')
    plt.close()
    chart_num += 1

    # --- VARIATION 08: Viridis Accessible ---
    fig, ax = plt.subplots(figsize=FIGSIZE_STANDARD, facecolor='white')

    colors = ['#21918c', '#440154']

    ax.fill_between(x, 0, data['cumulative_profit'], alpha=0.3, color=colors[0])
    ax.fill_between(x, 0, data['cumulative_expenses'], alpha=0.2, color=colors[1])

    ax.plot(x, data['cumulative_profit'], color=colors[0], linewidth=2.5, marker='o', markersize=6, label='Profit')
    ax.plot(x, data['cumulative_expenses'], color=colors[1], linewidth=2.5, marker='s', markersize=6, label='Expenses')

    uncertainty = data['cumulative_profit'] * 0.05
    ax.fill_between(x, data['cumulative_profit'] - uncertainty, data['cumulative_profit'] + uncertainty,
                    alpha=0.15, color=colors[0])

    ax.plot(x, trend_profit, color=colors[0], linewidth=1.5, linestyle='--', alpha=0.6)
    ax.plot(x, trend_expenses, color=colors[1], linewidth=1.5, linestyle='--', alpha=0.6)

    ax.set_xticks(x)
    ax.set_xticklabels(data['month_name'], fontsize=12)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_currency))

    apply_premium_style(fig, ax, 'Cumulative Performance Analysis',
                        subtitle='Colorblind-accessible visualization with uncertainty band')

    ax.legend(loc='upper left', frameon=True, edgecolor='#E0E0E0', fontsize=11)

    plt.subplots_adjust(top=0.82, bottom=0.12, left=0.10, right=0.95)
    plt.savefig(output_dir / f'py_{chart_num:02d}_viridis_accessible.png', dpi=DPI, facecolor='white')
    plt.close()

    print(f"  Created 8 Cumulative Analysis variations")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    print("=" * 70)
    print("FlowCast Professional Chart Generation - Python (STATE OF THE ART)")
    print("=" * 70)

    print("\nLoading sample data...")
    monthly_data = pd.read_csv(BASE_DIR / 'sample_data_monthly.csv')
    admin_data = pd.read_csv(BASE_DIR / 'sample_data_admin.csv')
    forecast_data = pd.read_csv(BASE_DIR / 'sample_data_forecast.csv')
    cumulative_data = pd.read_csv(BASE_DIR / 'sample_data_cumulative.csv')

    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False

    print("\nGenerating premium chart variations...")

    print("\n1. Operating Profit charts:")
    create_operating_profit_charts(monthly_data)

    print("\n2. Cost Breakdown charts:")
    create_cost_breakdown_charts(admin_data)

    print("\n3. Revenue Trends charts:")
    create_revenue_trends_charts(forecast_data)

    print("\n4. Cumulative Analysis charts:")
    create_cumulative_charts(cumulative_data)

    print("\n" + "=" * 70)
    print("Python chart generation complete!")
    print(f"Output saved to: {BASE_DIR}")
    print("\nFiles are numbered (py_01_, py_02_, etc.) for easy reference")
    print("=" * 70)


if __name__ == '__main__':
    main()
