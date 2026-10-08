@echo off
setlocal EnableExtensions
title Project 22 - Start frontend and backend

rem Always run from the directory containing this file, even when double-clicked.
cd /d "%~dp0"
if errorlevel 1 goto :error_dir

if not exist "package.json" (
    echo [ERROR] package.json not found. Keep run.bat in the repository root.
    goto :error
)

where node.exe >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is missing. Install Node.js 20 or newer first.
    goto :error
)
where npm.cmd >nul 2>&1
if errorlevel 1 (
    echo [ERROR] npm is missing. Install Node.js with npm first.
    goto :error
)

rem Node >= 20 is required by the workspaces.
set "NODE_MAJOR="
for /f "delims=" %%V in ('node -p "parseInt(process.versions.node,10)" 2^>nul') do set "NODE_MAJOR=%%V"
if not defined NODE_MAJOR (
    echo [ERROR] Cannot determine the Node.js version.
    goto :error
)
if %NODE_MAJOR% LSS 20 (
    echo [ERROR] Node.js 20 or newer is required. Current major: %NODE_MAJOR%.
    goto :error
)

rem Install on first launch, or if either workspace dev command is missing.
if not exist "node_modules\.bin\vite.cmd" goto :install
if not exist "node_modules\.bin\tsx.cmd" goto :install
rem Git pull may have changed package.json/package-lock without replacing node_modules.
call npm ls --depth=0 --silent >nul 2>&1
if errorlevel 1 goto :install
goto :launch

:install
echo [INFO] Installing dependencies with npm ci...
call npm ci
if errorlevel 1 (
    echo [ERROR] npm ci failed. Fix the installation error and run again.
    goto :error
)

:launch
if /I "%~1"=="--ci" goto :launch_ci
echo [INFO] Starting Backend at http://127.0.0.1:3001
start "Project 22 - Backend" /D "%CD%" cmd /k "npm run dev:backend"
if errorlevel 1 (
    echo [ERROR] Could not open the Backend window.
    goto :error
)

echo [INFO] Starting Frontend at http://localhost:5173
start "Project 22 - Frontend" /D "%CD%" cmd /k "npm run dev:frontend"
if errorlevel 1 (
    echo [ERROR] Could not open the Frontend window.
    goto :error
)

echo.
echo [OK] Frontend and Backend were launched in separate windows.
echo [INFO] Open http://localhost:5173 in your browser.
echo [INFO] To stop: press Ctrl+C in EACH server window.
exit /b 0

:launch_ci
rem Headless CI mode: use exactly the same npm scripts, but detach stdout/console.
echo [INFO] Starting Backend (headless CI) at http://127.0.0.1:3001
start "Project22-BE-CI" /D "%CD%" /B cmd /c "npm run dev:backend >NUL 2>&1"
if errorlevel 1 goto :error
echo [INFO] Starting Frontend (headless CI) at http://localhost:5173
start "Project22-FE-CI" /D "%CD%" /B cmd /c "npm run dev:frontend >NUL 2>&1"
if errorlevel 1 goto :error
echo [OK] CI launched frontend and backend. Verify readiness via HTTP.
exit /b 0

:error_dir
echo [ERROR] Cannot enter the repository directory.
:error
echo.
pause
exit /b 1
