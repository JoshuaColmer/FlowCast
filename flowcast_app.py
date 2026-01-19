#!/usr/bin/env python3
"""
FlowCast Report Generator - Simple GUI
A user-friendly interface for generating financial charts from Xero exports.

To run:
    pip install streamlit pandas openpyxl matplotlib xlsxwriter
    streamlit run flowcast_app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from datetime import datetime
from io import BytesIO
import zipfile
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="FlowCast Report Generator",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
    }
    .stDownloadButton > button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Color scheme
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72', 
    'tertiary': '#F18F01',
    'positive': '#4CAF50',
    'negative': '#E53935',
}


class FlowCastParser:
    """Parses Xero P&L exports into structured data."""
    
    def __init__(self, file_buffer):
        self.file_buffer = file_buffer
        self.raw_df = None
        self.months = []
        self.data = {}
        
    def parse(self) -> dict:
        """Parse the Excel file and extract all required data."""
        self.raw_df = pd.read_excel(self.file_buffer, header=None)
        self._extract_metadata()
        self._extract_months()
        self._extract_financial_data()
        self._extract_admin_breakdown()
        self._calculate_cumulative()
        return self.data
    
    def _extract_metadata(self):
        self.data['title'] = self.raw_df.iloc[0, 0] if pd.notna(self.raw_df.iloc[0, 0]) else "Profit and Loss"
        self.data['company'] = self.raw_df.iloc[1, 0] if pd.notna(self.raw_df.iloc[1, 0]) else "Company"
        self.data['period'] = self.raw_df.iloc[2, 0] if pd.notna(self.raw_df.iloc[2, 0]) else ""
        
    def _extract_months(self):
        header_row = self.raw_df.iloc[4, 1:].tolist()
        months = []
        for val in header_row:
            if pd.isna(val) or val == 'Year to date':
                continue
            if isinstance(val, datetime):
                months.append(val.strftime('%b %Y'))
            elif isinstance(val, str) and val.strip():
                months.append(val)
        self.months = months
        self.data['months'] = months
        self.num_months = len(months)
        
    def _find_row_by_label(self, label: str) -> int:
        for idx, val in enumerate(self.raw_df[0]):
            if pd.notna(val) and str(val).strip() == label:
                return idx
        return -1
    
    def _extract_row_values(self, row_idx: int) -> list:
        values = self.raw_df.iloc[row_idx, 1:self.num_months + 1].tolist()
        return [float(v) if pd.notna(v) else 0.0 for v in values]
    
    def _extract_financial_data(self):
        metrics = {
            'sales': 'Sales',
            'total_turnover': 'Total Turnover',
            'cost_of_sales': 'Total Cost of Sales',
            'gross_profit': 'Gross Profit',
            'total_admin_costs': 'Total Administrative Costs',
            'operating_profit': 'Operating Profit',
            'net_profit': 'Profit after Taxation',
        }
        for key, label in metrics.items():
            row_idx = self._find_row_by_label(label)
            if row_idx >= 0:
                self.data[key] = self._extract_row_values(row_idx)
            else:
                self.data[key] = [0.0] * self.num_months
                
    def _extract_admin_breakdown(self):
        admin_start = self._find_row_by_label('Administrative Costs')
        admin_end = self._find_row_by_label('Total Administrative Costs')
        
        if admin_start < 0 or admin_end < 0:
            self.data['admin_breakdown'] = {}
            return
        
        admin_items = {}
        for idx in range(admin_start + 1, admin_end):
            label = self.raw_df.iloc[idx, 0]
            if pd.notna(label) and str(label).strip():
                values = self._extract_row_values(idx)
                total = sum(values)
                if total != 0:
                    admin_items[str(label).strip()] = {
                        'monthly': values,
                        'total': total
                    }
        
        self.data['admin_breakdown'] = dict(
            sorted(admin_items.items(), key=lambda x: x[1]['total'], reverse=True)
        )
        
    def _calculate_cumulative(self):
        gross_c_row = self._find_row_by_label('Gross profit (c)')
        admin_c_row = self._find_row_by_label('Admin costs (c)')
        
        if gross_c_row >= 0:
            self.data['gross_profit_cumulative'] = self._extract_row_values(gross_c_row)
        else:
            self.data['gross_profit_cumulative'] = np.cumsum(self.data['gross_profit']).tolist()
            
        if admin_c_row >= 0:
            self.data['admin_costs_cumulative'] = self._extract_row_values(admin_c_row)
        else:
            self.data['admin_costs_cumulative'] = np.cumsum(self.data['total_admin_costs']).tolist()


class ChartGenerator:
    """Generates charts from parsed data."""
    
    def __init__(self, data: dict):
        self.data = data
        self.months = data['months']
        
    def create_operating_profit_chart(self) -> plt.Figure:
        fig, ax = plt.subplots(figsize=(10, 6))
        
        x = np.arange(len(self.months))
        width = 0.25
        
        gross_profit = self.data['gross_profit']
        admin_costs = self.data['total_admin_costs']
        operating_profit = self.data['operating_profit']
        
        ax.bar(x - width, operating_profit, width, label='Operating Profit',
               color=[COLORS['positive'] if v >= 0 else COLORS['negative'] for v in operating_profit])
        ax.bar(x, admin_costs, width, label='Total Administrative Costs', color=COLORS['secondary'])
        ax.bar(x + width, gross_profit, width, label='Gross Profit', color=COLORS['tertiary'])
        
        ax.set_ylabel('Amount (£)', fontsize=10)
        ax.set_title('Operating Profit', fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(self.months, rotation=45, ha='right', fontsize=9)
        ax.legend(loc='upper left', fontsize=9)
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'£{x:,.0f}'))
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def create_admin_costs_pie(self) -> plt.Figure:
        fig, ax = plt.subplots(figsize=(10, 8))
        
        admin_data = self.data['admin_breakdown']
        if not admin_data:
            ax.text(0.5, 0.5, 'No admin cost data available', ha='center', va='center')
            return fig
            
        labels = list(admin_data.keys())
        values = [item['total'] for item in admin_data.values()]
        
        colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))
        
        wedges, texts, autotexts = ax.pie(
            values, 
            labels=None,
            autopct=lambda pct: f'{pct:.1f}%' if pct > 3 else '',
            colors=colors,
            startangle=90,
            pctdistance=0.8
        )
        
        legend_labels = [f'{label}: £{val:,.0f}' for label, val in zip(labels, values)]
        ax.legend(wedges, legend_labels, title="", loc="center left", 
                 bbox_to_anchor=(-0.3, 0.5), fontsize=9)
        
        ax.set_title('Administrative Costs (Annual)', fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        return fig
    
    def create_gross_net_turnover_chart(self) -> plt.Figure:
        fig, ax = plt.subplots(figsize=(10, 6))
        
        x = range(len(self.months))
        
        gross_profit = self.data['gross_profit']
        turnover = self.data['total_turnover']
        net_profit = self.data.get('net_profit', self.data['operating_profit'])
        
        ax.fill_between(x, 0, turnover, alpha=0.5, label='Total Turnover', color=COLORS['primary'])
        ax.fill_between(x, 0, gross_profit, alpha=0.7, label='Gross Profit', color=COLORS['tertiary'])
        ax.plot(x, net_profit, label='Net Profit', color=COLORS['negative'], linewidth=2, marker='o', markersize=4)
        
        ax.set_ylabel('Amount (£)', fontsize=10)
        ax.set_title('Your Books and Balances', fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(self.months, rotation=45, ha='right', fontsize=9)
        ax.legend(loc='upper right', fontsize=9)
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'£{x:,.0f}'))
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def create_profit_expenses_trend(self) -> plt.Figure:
        fig, ax = plt.subplots(figsize=(10, 6))
        
        x = np.arange(len(self.months))
        
        gross_c = self.data['gross_profit_cumulative']
        admin_c = self.data['admin_costs_cumulative']
        
        ax.plot(x, gross_c, 'o-', label='Gross Profit (Cumulative)', color=COLORS['positive'], linewidth=2, markersize=6)
        ax.plot(x, admin_c, '^-', label='Admin Costs (Cumulative)', color=COLORS['negative'], linewidth=2, markersize=6)
        
        if len(x) > 1:
            z_gross = np.polyfit(x, gross_c, 1)
            p_gross = np.poly1d(z_gross)
            r2_gross = self._calculate_r2(gross_c, p_gross(x))
            ax.plot(x, p_gross(x), '--', color=COLORS['positive'], alpha=0.5,
                   label=f'Gross Profit Trend (R² = {r2_gross:.3f})')
            
            z_admin = np.polyfit(x, admin_c, 1)
            p_admin = np.poly1d(z_admin)
            r2_admin = self._calculate_r2(admin_c, p_admin(x))
            ax.plot(x, p_admin(x), '--', color=COLORS['negative'], alpha=0.5,
                   label=f'Admin Costs Trend (R² = {r2_admin:.3f})')
        
        ax.set_ylabel('Cumulative Amount (£)', fontsize=10)
        ax.set_title('Profit vs. Expenses Trend', fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(self.months, rotation=45, ha='right', fontsize=9)
        ax.legend(loc='upper left', fontsize=8)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'£{x:,.0f}'))
        ax.grid(axis='y', alpha=0.3)
        
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
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
    buf.seek(0)
    return buf.getvalue()


def create_excel_report(data: dict, charts: dict) -> bytes:
    """Create an Excel workbook with data and embedded charts."""
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        workbook = writer.book
        
        # Create summary sheet
        summary_data = {
            'Month': data['months'],
            'Sales': data['total_turnover'],
            'Gross Profit': data['gross_profit'],
            'Admin Costs': data['total_admin_costs'],
            'Operating Profit': data['operating_profit'],
        }
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(writer, sheet_name='Summary', index=False, startrow=2)
        
        worksheet = writer.sheets['Summary']
        worksheet.write(0, 0, data.get('company', 'Company'), workbook.add_format({'bold': True, 'font_size': 14}))
        worksheet.write(1, 0, data.get('period', ''))
        
        # Format as currency
        money_format = workbook.add_format({'num_format': '£#,##0.00'})
        for col in range(1, 5):
            worksheet.set_column(col, col, 15, money_format)
        worksheet.set_column(0, 0, 12)
        
        # Create admin breakdown sheet
        if data['admin_breakdown']:
            admin_data = {
                'Category': list(data['admin_breakdown'].keys()),
                'Annual Total': [item['total'] for item in data['admin_breakdown'].values()]
            }
            df_admin = pd.DataFrame(admin_data)
            df_admin.to_excel(writer, sheet_name='Admin Costs', index=False)
            
            worksheet2 = writer.sheets['Admin Costs']
            worksheet2.set_column(0, 0, 30)
            worksheet2.set_column(1, 1, 15, money_format)
    
    output.seek(0)
    return output.getvalue()


def create_zip_download(charts: dict, excel_data: bytes) -> bytes:
    """Create a ZIP file containing all outputs."""
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for name, fig in charts.items():
            img_bytes = fig_to_bytes(fig)
            zip_file.writestr(f'{name}.png', img_bytes)
        
        zip_file.writestr('FlowCast_Report.xlsx', excel_data)
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()


# =============================================================================
# MAIN APP
# =============================================================================

def main():
    # Header
    st.markdown('<p class="main-header">📊 FlowCast Report Generator</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Generate beautiful financial charts from your Xero export in seconds</p>', unsafe_allow_html=True)
    
    # File upload section
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        uploaded_file = st.file_uploader(
            "📁 Upload your Xero P&L Export (Excel file)",
            type=['xlsx', 'xls'],
            help="Export your Profit & Loss report from Xero as 'Current financial Year Month by Month'"
        )
    
    if uploaded_file is not None:
        try:
            # Parse the file
            with st.spinner('📊 Analysing your data...'):
                parser = FlowCastParser(uploaded_file)
                data = parser.parse()
            
            # Show success message with key stats
            st.success(f"✅ Successfully loaded data for **{data.get('company', 'your company')}**")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Months of Data", len(data['months']))
            with col2:
                st.metric("Admin Categories", len(data['admin_breakdown']))
            with col3:
                total_turnover = sum(data['total_turnover'])
                st.metric("Total Turnover", f"£{total_turnover:,.0f}")
            
            st.markdown("---")
            
            # Generate charts
            with st.spinner('🎨 Generating charts...'):
                generator = ChartGenerator(data)
                charts = {
                    'operating_profit': generator.create_operating_profit_chart(),
                    'admin_costs_pie': generator.create_admin_costs_pie(),
                    'gross_net_turnover': generator.create_gross_net_turnover_chart(),
                    'profit_expenses_trend': generator.create_profit_expenses_trend(),
                }
            
            # Display charts in a grid
            st.subheader("📈 Generated Charts")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.pyplot(charts['operating_profit'])
                st.download_button(
                    "⬇️ Download Operating Profit Chart",
                    fig_to_bytes(charts['operating_profit']),
                    "operating_profit.png",
                    "image/png"
                )
            
            with col2:
                st.pyplot(charts['admin_costs_pie'])
                st.download_button(
                    "⬇️ Download Admin Costs Chart",
                    fig_to_bytes(charts['admin_costs_pie']),
                    "admin_costs_pie.png",
                    "image/png"
                )
            
            col3, col4 = st.columns(2)
            
            with col3:
                st.pyplot(charts['gross_net_turnover'])
                st.download_button(
                    "⬇️ Download Books & Balances Chart",
                    fig_to_bytes(charts['gross_net_turnover']),
                    "gross_net_turnover.png",
                    "image/png"
                )
            
            with col4:
                st.pyplot(charts['profit_expenses_trend'])
                st.download_button(
                    "⬇️ Download Trend Chart",
                    fig_to_bytes(charts['profit_expenses_trend']),
                    "profit_expenses_trend.png",
                    "image/png"
                )
            
            # Download all section
            st.markdown("---")
            st.subheader("📦 Download All")
            
            col1, col2 = st.columns(2)
            
            with col1:
                excel_data = create_excel_report(data, charts)
                st.download_button(
                    "📊 Download Excel Report",
                    excel_data,
                    "FlowCast_Report.xlsx",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            
            with col2:
                zip_data = create_zip_download(charts, excel_data)
                st.download_button(
                    "🗂️ Download Everything (ZIP)",
                    zip_data,
                    "FlowCast_Complete.zip",
                    "application/zip",
                    use_container_width=True
                )
            
            # Close all figures to free memory
            for fig in charts.values():
                plt.close(fig)
                
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
            st.info("Please make sure you've uploaded a valid Xero Profit & Loss export in the 'Month by Month' format.")
    
    else:
        # Show instructions when no file uploaded
        st.markdown("---")
        st.subheader("📋 How to use")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **Step 1: Export from Xero**
            1. Go to Reporting → All Reports
            2. Select 'Profit and Loss'
            3. Choose 'Current financial Year Month by Month'
            4. Click 'Export to Excel'
            """)
        
        with col2:
            st.markdown("""
            **Step 2: Upload here**
            1. Click the upload button above
            2. Select your downloaded Excel file
            3. Wait for processing
            """)
        
        with col3:
            st.markdown("""
            **Step 3: Download results**
            1. Review the generated charts
            2. Download individual charts or
            3. Download everything as a ZIP
            """)
        
        st.markdown("---")
        st.info("💡 **Tip:** The charts will match your data automatically - no manual formatting needed!")


if __name__ == '__main__':
    main()
