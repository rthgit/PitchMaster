@echo off
title Pitch Master - Stop
echo Stopping Pitch Master...
taskkill /f /im streamlit.exe 2>nul
echo Done.
pause
