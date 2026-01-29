"""
FlowCast API Backend
FastAPI server that provides endpoints for file upload, analysis, and report generation.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import FlowCast modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import tempfile
import io
import base64

# Import FlowCast modules
from parser import FlowCastParser
from metrics import MetricsCalculator
from forecaster import Forecaster
from insights import InsightGenerator
from charts import ChartGenerator, fig_to_bytes
from exporters.excel import create_excel_report, create_zip_download

app = FastAPI(
    title="FlowCast API",
    description="Financial health check in 60 seconds",
    version="2.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "https://*.vercel.app",  # Vercel preview deployments
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",  # All Vercel subdomains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for session data
sessions = {}


class AnalysisResponse(BaseModel):
    session_id: str
    company: str
    metrics: dict
    health_summary: dict
    insights: list
    forecast: dict
    charts: dict  # Base64 encoded chart images


class ExportRequest(BaseModel):
    session_id: str
    format: str  # 'excel', 'pdf', 'pptx', 'zip'
    currency: str = '£'


@app.get("/")
async def root():
    return {"message": "FlowCast API v2.0", "status": "healthy"}


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...), currency: str = "£"):
    """Upload and analyze a Xero P&L Excel file."""

    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Please upload an Excel file (.xlsx or .xls)")

    try:
        # Save uploaded file temporarily
        content = await file.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        try:
            # Parse the file
            parser = FlowCastParser(tmp_path)
            data = parser.parse()

            # Calculate metrics
            metrics_calc = MetricsCalculator(data)
            metrics = metrics_calc.calculate_all()
            health_summary = metrics_calc.get_health_summary()

            # Generate forecast
            forecaster = Forecaster(data, horizon=6)
            forecast_data = forecaster.generate_forecast()

            # Generate insights
            insight_gen = InsightGenerator(data, metrics, forecast_data)
            insights = insight_gen.generate_insights()

            # Generate charts
            generator = ChartGenerator(data, forecast_data, currency=currency)
            charts_fig = {
                'operating_profit': generator.create_operating_profit_chart(),
                'admin_costs_pie': generator.create_admin_costs_pie(),
                'revenue_profit_trend': generator.create_revenue_profit_trend(),
                'profit_expenses_trend': generator.create_profit_expenses_trend(),
            }

            # Convert charts to base64
            charts_b64 = {}
            for name, fig in charts_fig.items():
                img_bytes = fig_to_bytes(fig)
                charts_b64[name] = base64.b64encode(img_bytes).decode('utf-8')
                import matplotlib.pyplot as plt
                plt.close(fig)

            # Generate session ID
            import uuid
            session_id = str(uuid.uuid4())[:8]

            # Store session data
            sessions[session_id] = {
                'data': data,
                'metrics': metrics,
                'health_summary': health_summary,
                'forecast_data': forecast_data,
                'insights': insights,
                'charts_fig': charts_fig,
                'currency': currency,
            }

            # Prepare response
            return {
                'session_id': session_id,
                'company': data.get('company', 'Unknown'),
                'metrics': _serialize_metrics(metrics),
                'health_summary': health_summary,
                'insights': insights,
                'forecast': _serialize_forecast(forecast_data),
                'charts': charts_b64,
            }

        finally:
            # Clean up temp file
            os.unlink(tmp_path)

    except Exception as e:
        import traceback
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}\n{traceback.format_exc()}")


@app.get("/api/export/{session_id}/{format}")
async def export_report(session_id: str, format: str):
    """Export report in various formats."""

    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found. Please upload a file first.")

    session = sessions[session_id]
    data = session['data']
    metrics = session['metrics']
    insights = session['insights']
    forecast_data = session['forecast_data']
    currency = session['currency']

    try:
        if format == 'excel':
            # Regenerate charts for Excel
            generator = ChartGenerator(data, forecast_data, currency=currency)
            charts = {
                'operating_profit': generator.create_operating_profit_chart(),
                'admin_costs_pie': generator.create_admin_costs_pie(),
                'revenue_profit_trend': generator.create_revenue_profit_trend(),
                'profit_expenses_trend': generator.create_profit_expenses_trend(),
            }

            excel_data = create_excel_report(data, charts, metrics, forecast_data)

            # Close figures
            import matplotlib.pyplot as plt
            for fig in charts.values():
                plt.close(fig)

            return StreamingResponse(
                io.BytesIO(excel_data),
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={"Content-Disposition": "attachment; filename=FlowCast_Report.xlsx"}
            )

        elif format == 'zip':
            generator = ChartGenerator(data, forecast_data, currency=currency)
            charts = {
                'operating_profit': generator.create_operating_profit_chart(),
                'admin_costs_pie': generator.create_admin_costs_pie(),
                'revenue_profit_trend': generator.create_revenue_profit_trend(),
                'profit_expenses_trend': generator.create_profit_expenses_trend(),
            }

            excel_data = create_excel_report(data, charts, metrics, forecast_data)

            # Try to create PDF
            pdf_data = None
            try:
                from exporters.pdf import create_pdf_report
                pdf_data = create_pdf_report(data, metrics, insights, forecast_data, currency)
            except:
                pass

            # Try to create PPTX
            pptx_data = None
            try:
                from exporters.pptx import create_pptx_report
                pptx_data = create_pptx_report(data, metrics, insights, charts, forecast_data, currency)
            except:
                pass

            zip_data = create_zip_download(charts, excel_data, pdf_data, pptx_data)

            import matplotlib.pyplot as plt
            for fig in charts.values():
                plt.close(fig)

            return StreamingResponse(
                io.BytesIO(zip_data),
                media_type="application/zip",
                headers={"Content-Disposition": "attachment; filename=FlowCast_Complete.zip"}
            )

        else:
            raise HTTPException(status_code=400, detail=f"Unknown format: {format}")

    except Exception as e:
        import traceback
        raise HTTPException(status_code=500, detail=f"Error generating export: {str(e)}")


def _serialize_metrics(metrics: dict) -> dict:
    """Convert metrics to JSON-serializable format."""
    result = {}
    for key, value in metrics.items():
        if isinstance(value, dict):
            result[key] = {k: (float(v) if hasattr(v, '__float__') else v) for k, v in value.items()}
        else:
            result[key] = float(value) if hasattr(value, '__float__') else value
    return result


def _serialize_forecast(forecast: dict) -> dict:
    """Convert forecast data to JSON-serializable format."""
    result = {}
    for key, value in forecast.items():
        if hasattr(value, 'tolist'):  # numpy array
            result[key] = value.tolist()
        elif isinstance(value, list):
            result[key] = [float(v) if hasattr(v, '__float__') else v for v in value]
        else:
            result[key] = value
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
