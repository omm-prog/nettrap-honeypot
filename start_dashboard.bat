@echo off
echo Starting NetTrap Attack Map Dashboard...
echo.

REM Activate virtual environment
call honeypot_env\Scripts\activate.bat

REM Run just the dashboard
python -c "from src.attack_map import RealTimeAttackMap; am = RealTimeAttackMap(); am.start_dashboard()"

pause