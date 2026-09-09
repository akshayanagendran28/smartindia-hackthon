@echo off
echo ========================================================
echo   SCHEME SATHI - Smart India Hackathon 2026 (SIH26092)
echo   AI-Driven Scheme Matching for Marginalized Founders
echo ========================================================
echo.
echo Launching Backend and Frontend in separate windows...
start "Scheme Sathi Backend (FastAPI)" cmd /k "start_backend.bat"
timeout /t 3 /nobreak >nul
start "Scheme Sathi Frontend (Vite + React)" cmd /k "start_frontend.bat"
echo.
echo Both servers initiated!
echo Backend:  http://127.0.0.1:8008 (API Docs: http://127.0.0.1:8008/docs)
echo Frontend: http://127.0.0.1:5173
echo.
pause
