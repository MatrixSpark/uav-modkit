@echo off
REM UAV ModKit ROS 2 Environment Setup via WSL2
REM Use this from Windows PowerShell/cmd to avoid using bash 'source' in PowerShell.

setlocal

echo.
echo ==========================================
echo UAV ModKit - WSL2 Environment Setup
echo ==========================================

REM Resolve repository path (directory of this script).
set "REPO_WIN=%~dp0"
if "%REPO_WIN:~-1%"=="\" set "REPO_WIN=%REPO_WIN:~0,-1%"

REM Convert Windows path to WSL path.
for /f "delims=" %%P in ('wsl wslpath "%REPO_WIN%"') do set "REPO_WSL=%%P"
if not defined REPO_WSL (
    echo ERROR: Could not resolve repository path in WSL.
    echo Ensure WSL is installed and available: wsl -l -q
    exit /b 1
)

REM Validate setup scripts and print quick status.
wsl bash -lc "source /opt/ros/jazzy/setup.bash && cd '%REPO_WSL%' && source install/setup.bash && echo ROS_DISTRO=$ROS_DISTRO && ros2 pkg prefix camera_sensor"
if errorlevel 1 (
    echo.
    echo ERROR: Failed to source ROS/workspace in WSL.
    exit /b 1
)

echo.
echo Environment is ready in WSL.
echo For an interactive WSL shell in this repo, run:
echo   wsl bash -lc "source /opt/ros/jazzy/setup.bash && cd '%REPO_WSL%' && source install/setup.bash && exec bash"
echo.

endlocal