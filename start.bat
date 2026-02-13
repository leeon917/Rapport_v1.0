@echo off
echo Starting Rapport Backend and Frontend...

echo.
echo Starting Backend...
cd backend
if not exist .env (
    echo Creating .env from .env.example...
    copy .env.example .env
)
start "Rapport Backend" cmd /k "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo.
echo Starting Frontend (uni-app H5)...
cd ..\frontend
if not exist .env (
    echo Creating .env from .env.example...
    copy .env.example .env
)
echo Installing dependencies...
call npm install
echo.
echo Starting dev server...
start "Rapport Frontend" cmd /k "npm run dev:h5"

echo.
echo Both services are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/docs
