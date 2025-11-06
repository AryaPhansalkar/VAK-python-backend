@Echo Off
SetLocal EnableDelayedExpansion

REM =======================================================
REM  Project Setup Script - make.cmd
REM  Usage:
REM      make setup        → Installs all dependencies
REM =======================================================

Set Target=%~1

Set Targets=
For /F "Delims=:" %%I in ('FindStr /R "^:" "%~f0"') Do Set Targets=!Targets! %%I
For %%A in (!Targets!) Do (
    If /I "%Target%"=="%%A" Call :%%A & Exit /B
)
GoTo :Help


:Setup
    echo.
    echo  Starting project setup...
    echo ---------------------------------------

    REM Check for Python
    python --version >nul 2>&1
    if errorlevel 1 (
        echo  Python not found! Please install Python 3.8 or above.
        exit /b 1
    )

    REM Check for requirements.txt
    if not exist requirements.txt (
        echo  requirements.txt not found in this directory!
        exit /b 1
    )

    echo  Upgrading pip...
    python -m pip install --upgrade pip

    echo  Installing dependencies from requirements.txt...
    python -m pip install -r requirements.txt

    if errorlevel 1 (
        echo  Installation failed! Check your requirements.txt or internet connection.
        exit /b 1
    )

    echo.
    echo All dependencies installed successfully!
    echo ---------------------------------------
    exit /b 0


:Help
    echo.
    echo   Usage:
    echo   make setup      Install all dependencies from requirements.txt
    echo.
    exit /b 1
