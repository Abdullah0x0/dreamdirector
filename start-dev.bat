@echo off
echo 🎬 DreamDirector - Windows Development Setup
echo UC Berkeley AI Hackathon 2025
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo.
    echo 📥 Please install Python from: https://python.org/downloads/
    echo ✅ Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed or not in PATH
    echo.
    echo 📥 Please install Node.js from: https://nodejs.org/
    echo.
    pause
    exit /b 1
)

echo ✅ Python and Node.js are available
echo.

REM Install frontend dependencies
echo 📦 Installing frontend dependencies...
if not exist "node_modules" (
    echo Installing Node.js packages...
    npm install
) else (
    echo Node modules already installed
)

REM Install backend dependencies  
echo 📦 Installing backend dependencies...
if not exist "backend\venv" (
    echo Creating Python virtual environment...
    cd backend
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
    cd ..
) else (
    echo Virtual environment already exists
)

echo.
echo 🚀 Starting development servers...
echo.

REM Start backend server
echo 🔧 Starting FastAPI backend on http://localhost:8000
cd backend
call venv\Scripts\activate
start /b python app.py
cd ..

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend server
echo 🎨 Starting React frontend on http://localhost:3000
start /b npm run dev

echo.
echo ✅ Development environment is ready!
echo.
echo 📍 Frontend: http://localhost:3000
echo 📍 Backend API: http://localhost:8000
echo 📍 API Docs: http://localhost:8000/docs
echo.
echo 💡 The UI will work in demo mode even without the full AI backend
echo 💡 To use full AI features, ensure your .env file has GOOGLE_API_KEY
echo.
echo Press any key to stop all servers...
pause >nul

REM Kill background processes
taskkill /f /im python.exe 2>nul
taskkill /f /im node.exe 2>nul
echo 🛑 Development servers stopped 