@echo off
echo Starting Plaksha UI...

REM ---- 1. Activate virtual environment ----
call %~dp0.venv\Scripts\activate

REM ---- 2. Start the NiceGUI app ----
start "" python "%~dp0main.py"

REM ---- 3. Wait a moment for server to start ----
timeout /t 2 >nul

REM ---- 4. Open Chrome in a new window ----
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --new-window "http://127.0.0.1:8080"

exit
