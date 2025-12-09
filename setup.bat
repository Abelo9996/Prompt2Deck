@echo off
REM Prompt2Deck Quick Setup Script for Windows

echo Setting up Prompt2Deck...

REM Backend Setup
echo.
echo Setting up Backend...
cd backend

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
    echo Please edit backend\.env and add your OPENAI_API_KEY
)

cd ..

REM Frontend Setup
echo.
echo Setting up Frontend...
cd frontend

if not exist "node_modules" (
    echo Installing Node.js dependencies...
    call npm install
)

if not exist ".env.local" (
    echo Creating .env.local file...
    copy .env.example .env.local
)

cd ..

REM Success message
echo.
echo Setup complete!
echo.
echo To start the backend:
echo   cd backend
echo   venv\Scripts\activate
echo   python main.py
echo.
echo To start the frontend:
echo   cd frontend
echo   npm run dev
echo.
echo Don't forget to add your OPENAI_API_KEY to backend\.env
echo.

pause
