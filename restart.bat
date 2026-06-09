@echo off
title Pitch Master - Restart
echo Restarting Pitch Master...
taskkill /f /im streamlit.exe 2>nul
timeout /t 2 /nobreak >nul
cd /d "%~dp0"
call .venv\Scripts\activate
streamlit run app.py --server.port 8501 --server.headless false
