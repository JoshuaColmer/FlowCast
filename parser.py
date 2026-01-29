"""
FlowCast Parser Module
Parses Xero P&L exports into structured data.
"""

import pandas as pd
import numpy as np
from datetime import datetime


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
