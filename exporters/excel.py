"""
FlowCast Excel Exporter
Creates Excel workbooks with financial data and charts.
"""

import pandas as pd
from io import BytesIO
import zipfile
from charts import fig_to_bytes


def create_excel_report(data: dict, charts: dict = None, metrics: dict = None,
                        forecast_data: dict = None) -> bytes:
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
        worksheet.write(0, 0, data.get('company', 'Company'),
                       workbook.add_format({'bold': True, 'font_size': 14}))
        worksheet.write(1, 0, data.get('period', ''))

        # Format as currency
        money_format = workbook.add_format({'num_format': '#,##0.00'})
        for col in range(1, 5):
            worksheet.set_column(col, col, 15, money_format)
        worksheet.set_column(0, 0, 12)

        # Create metrics sheet if metrics provided
        if metrics:
            metrics_data = {
                'Metric': [],
                'Value': [],
                'Status': []
            }
            for key, value in metrics.items():
                if isinstance(value, dict) and 'value' in value:
                    metrics_data['Metric'].append(key.replace('_', ' ').title())
                    metrics_data['Value'].append(value['value'])
                    metrics_data['Status'].append(value.get('status', ''))

            if metrics_data['Metric']:
                df_metrics = pd.DataFrame(metrics_data)
                df_metrics.to_excel(writer, sheet_name='Metrics', index=False)

                worksheet_metrics = writer.sheets['Metrics']
                worksheet_metrics.set_column(0, 0, 25)
                worksheet_metrics.set_column(1, 1, 15)
                worksheet_metrics.set_column(2, 2, 10)

        # Create forecast sheet if forecast data provided
        if forecast_data and forecast_data.get('months'):
            forecast_sheet_data = {
                'Month': forecast_data['months'],
            }
            if 'revenue' in forecast_data:
                forecast_sheet_data['Revenue (Forecast)'] = forecast_data['revenue']['values']
            if 'gross_profit' in forecast_data:
                forecast_sheet_data['Gross Profit (Forecast)'] = forecast_data['gross_profit']['values']
            if 'operating_profit' in forecast_data:
                forecast_sheet_data['Operating Profit (Forecast)'] = forecast_data['operating_profit']['values']

            df_forecast = pd.DataFrame(forecast_sheet_data)
            df_forecast.to_excel(writer, sheet_name='Forecast', index=False)

            worksheet_forecast = writer.sheets['Forecast']
            worksheet_forecast.set_column(0, 0, 12)
            for col in range(1, len(forecast_sheet_data)):
                worksheet_forecast.set_column(col, col, 20, money_format)

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


def create_zip_download(charts: dict, excel_data: bytes, pdf_data: bytes = None,
                        pptx_data: bytes = None) -> bytes:
    """Create a ZIP file containing all outputs."""
    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Add chart images
        for name, fig in charts.items():
            img_bytes = fig_to_bytes(fig)
            zip_file.writestr(f'{name}.png', img_bytes)

        # Add Excel report
        zip_file.writestr('FlowCast_Report.xlsx', excel_data)

        # Add PDF if provided
        if pdf_data:
            zip_file.writestr('FlowCast_Report.pdf', pdf_data)

        # Add PowerPoint if provided
        if pptx_data:
            zip_file.writestr('FlowCast_Report.pptx', pptx_data)

    zip_buffer.seek(0)
    return zip_buffer.getvalue()
