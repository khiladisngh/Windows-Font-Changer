@echo off
echo Building Windows Font Changer Executable
echo ========================================
echo.

REM Check if uv is installed
where uv >nul 2>&1
if %errorLevel% neq 0 (
    echo Error: uv is not installed. Please install uv first.
    echo Run: pip install uv
    pause
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
uv sync --dev

REM Run ruff checks
echo.
echo Running code quality checks...
uv run ruff check .
if %errorLevel% neq 0 (
    echo Error: Ruff check failed. Please fix the issues and try again.
    pause
    exit /b 1
)

REM Build executable
echo.
echo Building executable...
uv run pyinstaller windows_font_changer.spec --clean

if exist "dist\Windows Font Changer.exe" (
    echo.
    echo ========================================
    echo Build successful!
    echo Executable location: dist\Windows Font Changer.exe
    echo ========================================
) else (
    echo.
    echo Build failed!
)

pause 