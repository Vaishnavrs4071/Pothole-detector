@echo off
echo ============================================================
echo Starting Pothole Detection Web Server
echo ============================================================
echo.
echo The server will start at http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
cd /d "%~dp0"
python app.py
pause
