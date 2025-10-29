@echo off
echo Starting NetTrap Honeypot...
echo.

REM Activate virtual environment
call honeypot_env\Scripts\activate.bat

REM Run the honeypot
python -m src.honeypot

pause