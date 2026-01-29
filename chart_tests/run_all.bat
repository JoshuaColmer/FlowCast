@echo off
REM =============================================================================
REM FlowCast Professional Chart Generation - Run All
REM Generates all Python and R chart variations
REM =============================================================================

echo.
echo ============================================================
echo FlowCast Professional Chart Generation
echo ============================================================
echo.

REM Navigate to script directory
cd /d "%~dp0"

REM Step 1: Generate sample data
echo [1/3] Generating sample data...
python generate_sample_data.py
if %ERRORLEVEL% neq 0 (
    echo ERROR: Sample data generation failed!
    pause
    exit /b 1
)
echo      Sample data generated successfully.
echo.

REM Step 2: Generate Python charts
echo [2/3] Generating Python charts...
python python_charts.py
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python chart generation failed!
    pause
    exit /b 1
)
echo      Python charts generated successfully.
echo.

REM Step 3: Generate R charts
echo [3/3] Generating R charts...
Rscript r_charts.R
if %ERRORLEVEL% neq 0 (
    echo WARNING: R chart generation may have had issues.
    echo          Check the R output above for details.
)
echo      R charts generated.
echo.

REM Summary
echo ============================================================
echo Chart Generation Complete!
echo ============================================================
echo.
echo Output directories:
echo   - 01_operating_profit\
echo   - 02_cost_breakdown\
echo   - 03_revenue_trends\
echo   - 04_cumulative_analysis\
echo.
echo Review the generated PNG files for:
echo   [x] Clear, readable labels and titles
echo   [x] Professional color palettes
echo   [x] Proper currency formatting
echo   [x] High resolution (450 DPI)
echo   [x] Consistent styling within each variation
echo   [x] Annual report quality appearance
echo.

REM Open output directory
echo Opening output folder...
start "" "%~dp0"

pause
