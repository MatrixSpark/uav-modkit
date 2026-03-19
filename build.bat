@echo off
REM UAV ModKit ROS 2 Build Script for Windows
REM This script builds all ROS 2 packages in the workspace

setlocal enabledelayedexpansion

echo.
echo ==========================================
echo UAV ModKit - ROS 2 Build Script (Windows)
echo ==========================================

REM Check if ROS 2 is set up
if not defined ROS_DISTRO (
    echo ERROR: ROS 2 is not sourced!
    echo Please run: call C:\opt\ros2\humble\local_setup.bat
    echo Or if using WSL2, open WSL terminal and run build.sh
    exit /b 1
)

echo ROS 2 Distribution: %ROS_DISTRO%

REM Create workspace
if not exist \"colcon_ws\\src\" (
    mkdir colcon_ws\\src
    echo Created colcon workspace
)

cd /d %~dp0

REM Build packages
echo.
echo Building packages with colcon...
call colcon build --symlink-install

echo.
echo ==========================================
echo Build completed successfully!
echo ==========================================
echo.
echo Next steps:
echo   - Source the workspace:
echo     call install\\setup.bat
echo   - List available packages:
echo     ros2 pkg list
echo.

endlocal
