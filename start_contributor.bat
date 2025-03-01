@echo off
cd /d %~dp0
call pm2 delete green-contributor
call pm2 start index.js --name green-contributor