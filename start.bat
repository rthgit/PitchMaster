@echo off
title Pitch Master
echo ========================================
echo   Pitch Master - Starting...
echo ========================================
echo.

cd /d "%~dp0"

if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

echo Activating environment...
call .venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt -q

echo.
echo Starting Pitch Master on http://localhost:8501
echo Press Ctrl+C to stop
echo.
streamlit run app.py --server.port 8501 --server.headless false
