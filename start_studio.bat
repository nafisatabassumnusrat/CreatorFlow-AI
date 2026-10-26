@echo off
title CreatorFlow AI Studio - Local Server
cd /d "%~dp0"
echo ========================================================
echo   CreatorFlow AI Studio - One-Click Launcher
echo ========================================================
echo.
set PY_CMD=

REM 1. Check if python is in PATH
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PY_CMD=python
    goto :FOUND
)

REM 2. Check if py launcher is available
py --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PY_CMD=py
    goto :FOUND
)

REM 3. Check common AppData Python locations
if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" (
    set "PY_CMD=%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
    goto :FOUND
)
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set "PY_CMD=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    goto :FOUND
)
if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    set "PY_CMD=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    goto :FOUND
)

REM 4. Check Program Files locations
if exist "C:\Program Files\Python313\python.exe" (
    set "PY_CMD=C:\Program Files\Python313\python.exe"
    goto :FOUND
)
if exist "C:\Program Files\Python312\python.exe" (
    set "PY_CMD=C:\Program Files\Python312\python.exe"
    goto :FOUND
)

:NOT_FOUND
echo.
echo [ERROR] Python was not found in PATH or standard installation folders.
echo Please install Python 3.10+ from https://www.python.org/
echo Check the box "Add python.exe to PATH" during installation.
echo.
pause
exit /b 1

:FOUND
echo Python found! Using: %PY_CMD%
echo.
echo [2/3] Installing/verifying dependencies (FastAPI, Uvicorn, Pillow, FFmpeg)...
%PY_CMD% -m pip install fastapi uvicorn pydantic pillow httpx edge-tts imageio-ffmpeg

echo.
echo [3/3] Launching Studio server and opening browser...
echo.
echo ========================================================
echo   Studio running at: http://127.0.0.1:8000
echo   Keep this black window open while using CreatorFlow!
echo ========================================================
echo.
start http://127.0.0.1:8000/
%PY_CMD% -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
pause
