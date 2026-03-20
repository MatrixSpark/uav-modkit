@echo off
REM UAV ModKit ROS 2 Build Script via WSL2
REM Use this from Windows PowerShell/cmd when ROS 2 is installed in WSL.

setlocal

echo.
echo ==========================================
echo UAV ModKit - WSL2 Build Script (Windows)
echo ==========================================

REM Resolve repository path (directory of this script).
set "REPO_WIN=%~dp0"
if "%REPO_WIN:~-1%"=="\" set "REPO_WIN=%REPO_WIN:~0,-1%"

REM Convert Windows path to WSL path safely.
for /f "delims=" %%P in ('wsl wslpath "%REPO_WIN%"') do set "REPO_WSL=%%P"
if not defined REPO_WSL (
    echo ERROR: Could not resolve repository path in WSL.
    echo Ensure WSL is installed and available: wsl -l -q
    exit /b 1
)

echo Building in WSL path: %REPO_WSL%

REM Build canonical package directories directly to avoid duplicate names in colcon_ws/src.
wsl bash -lc "source /opt/ros/jazzy/setup.bash && cd '%REPO_WSL%' && colcon build --symlink-install --base-paths camera imu lidar power"
if errorlevel 1 (
    echo.
    echo ERROR: WSL build failed.
    echo Verify ROS 2 Jazzy exists in WSL: ls /opt/ros/jazzy
    exit /b 1
)

echo.
echo ==========================================
echo Build completed successfully in WSL.
echo ==========================================
echo.
echo Next step from Windows PowerShell/cmd:
echo   .\setup_wsl.bat
echo.
echo Or manually inside WSL:
echo   source /opt/ros/jazzy/setup.bash
echo   cd %REPO_WSL%
echo   source install/setup.bash
echo.

endlocal