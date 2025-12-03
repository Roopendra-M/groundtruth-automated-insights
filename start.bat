@echo off
echo Starting Full Stack Application...
echo.
echo Starting Backend Server in new window...
start "Backend Server" cmd /k "cd backend && python -m venv venv && call venv\Scripts\activate && pip install -r requirements.txt && python app.py"
timeout /t 5 /nobreak >nul
echo.
echo Starting Frontend Server in new window...
start "Frontend Server" cmd /k "cd frontend && npm install && npm start"
echo.
echo Both servers are starting...
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
pause

