@echo off
echo Windows Font Changer
echo ====================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running with administrator privileges...
) else (
    echo WARNING: Not running as administrator!
    echo The application requires administrator privileges to modify system fonts.
    echo Please right-click this file and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

REM Check if uv is installed
where uv >nul 2>&1
if %errorLevel% neq 0 (
    echo uv is not installed. Installing uv...
    pip install uv
)

REM Run the application
echo Starting Windows Font Changer...
uv run python -m windows_font_changer

pause 