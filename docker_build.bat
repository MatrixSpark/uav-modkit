@echo off
setlocal

docker build -f docker\Dockerfile -t uav-modkit:jazzy .
if errorlevel 1 exit /b 1

echo Docker image built: uav-modkit:jazzy
endlocal
