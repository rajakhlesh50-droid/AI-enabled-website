@echo off
setlocal

set "PROJECT_DIR=%~dp0"
if not exist "%PROJECT_DIR%.venv\Scripts\python.exe" (
    echo Creating the project Python environment...
    py -3 -m venv "%PROJECT_DIR%.venv"
    if errorlevel 1 (
        echo Could not create the Python environment. Install Python 3 and try again.
        pause
        exit /b 1
    )
)
set "PYTHON_EXE=%PROJECT_DIR%.venv\Scripts\python.exe"

echo Checking Python dependencies...
"%PYTHON_EXE%" -c "import flask, flask_cors, jwt, dotenv" >nul 2>&1
if errorlevel 1 (
    echo Installing project dependencies...
    "%PYTHON_EXE%" -m pip install -r "%PROJECT_DIR%requirements.txt"
    if errorlevel 1 (
        echo Could not install dependencies. Check Python and internet access.
        pause
        exit /b 1
    )
)

echo Starting AI University website...
start "AI University Backend" /D "%PROJECT_DIR%backend" "%PYTHON_EXE%" app.py

echo Waiting for the local server...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ready = $false; for ($i = 0; $i -lt 30; $i++) { try { $response = Invoke-WebRequest -UseBasicParsing -Uri 'http://127.0.0.1:5000/' -TimeoutSec 1; if ($response.StatusCode -eq 200) { $ready = $true; break } } catch { Start-Sleep -Seconds 1 } }; if (-not $ready) { exit 1 }"
if errorlevel 1 (
    echo The website did not start. Check whether port 5000 is already in use.
    pause
    exit /b 1
)

echo Opening http://127.0.0.1:5000/
start "" "http://127.0.0.1:5000/"
echo Website is ready. Admin sign-in: http://127.0.0.1:5000/login
endlocal
