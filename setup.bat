@echo off
echo ===================================================
echo   SemantiHire AI - Setup Script
echo ===================================================
echo.

echo [1/4] Setting up Python virtual environment in backend...
cd backend
python -m venv venv
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to create virtual environment. Make sure Python 3.10+ is installed and on your PATH.
    pause
    exit /b %errorlevel%
)

echo.
echo [2/4] Activating virtual environment and installing dependencies...
call .\venv\Scripts\activate
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install Python dependencies.
    pause
    exit /b %errorlevel%
)

echo.
echo [3/4] Downloading spaCy English model...
python -m spacy download en_core_web_sm
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to download spaCy language model.
    pause
    exit /b %errorlevel%
)

echo.
echo [4/4] Creating environment file...
if not exist .env (
    copy .env.example .env
)
cd ..

echo.
echo ===================================================
echo   Backend setup complete!
echo ===================================================
echo.
echo To run the Backend:
echo   cd backend
echo   .\venv\Scripts\activate
echo   uvicorn app.main:app --reload --port 8000
echo.
echo To run the Frontend:
echo   cd frontend
echo   npm install
echo   npm run dev
echo.
echo ===================================================
pause
