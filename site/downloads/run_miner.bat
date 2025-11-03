@echo off
set NODE=node.banncoin.org:17536
set WALLET=%1
if "%WALLET%"=="" (
  set /p WALLET=Enter your BNC address (bnc1...):
)
where python >nul 2>&1 || (
  echo Python 3 is required. Install: https://www.python.org/downloads/
  pause & exit /b 1
)
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "Invoke-WebRequest -UseBasicParsing https://banncoin.org/downloads/banncoin_miner.py -OutFile banncoin_miner.py"
python banncoin_miner.py --node %NODE% --wallet %WALLET%
pause
