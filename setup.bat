@echo off
echo Installing NetTrap Honeypot...
echo.

REM Create virtual environment
python -m venv honeypot_env
call honeypot_env\Scripts\activate.bat

REM Install requirements
pip install -r requirements.txt

REM Create necessary directories
if not exist logs mkdir logs
if not exist config mkdir config

echo.
echo ✅ Setup completed successfully!
echo.
echo To start the honeypot, run:
echo start_honeypot.bat
echo.
pause