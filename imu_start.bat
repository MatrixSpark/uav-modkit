@echo off
REM Launch IMU stack from Windows via WSL2.

setlocal

set "REPO_WIN=%~dp0"
if "%REPO_WIN:~-1%"=="\" set "REPO_WIN=%REPO_WIN:~0,-1%"

for /f "delims=" %%P in ('wsl wslpath "%REPO_WIN%"') do set "REPO_WSL=%%P"
if not defined REPO_WSL (
    echo ERROR: Could not resolve repository path in WSL.
    exit /b 1
)

echo Launching IMU from %REPO_WSL%
wsl bash -lc "source /opt/ros/jazzy/setup.bash && cd '%REPO_WSL%' && source install/setup.bash && ros2 launch '%REPO_WSL%/launch/imu_auto.launch.py' %*"

endlocal
