@echo off
echo Starting GitHub Green Contributor...

:: Change to script directory
cd /d "%~dp0"

:: Start the process
echo Starting process...
call npm install
call pm2 delete green-contributor > nul 2>&1
call pm2 start index.js --name "green-contributor"

:: Show status
echo Checking status...
call pm2 status
call pm2 save

echo.
echo Process started! Check GitHub for contributions.
echo Press any key to close this window...
pause > nul
