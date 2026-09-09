@echo off
echo Starting Scheme Sathi FastAPI Backend on Port 8008...
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8008 --reload
pause
