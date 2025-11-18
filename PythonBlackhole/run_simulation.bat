@echo off
echo ========================================
echo   BLACK HOLE SIMULATION LAUNCHER
echo ========================================
echo.
echo Checking dependencies...
python -c "import numpy, colorama" 2>nul
if errorlevel 1 (
    echo Installing required packages...
    pip install numpy colorama
)
echo.
echo Starting simulation...
echo.
python black_hole_sim.py
pause
