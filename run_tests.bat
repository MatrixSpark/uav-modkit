@echo off
REM UAV ModKit Test Campaign 
REM This script runs all unit tests for the UAV ModKit project

echo ==========================================
echo UAV ModKit - Test Runner (Windows)
echo ==========================================

REM Check if we're in the right directory
if not exist "test\" (
    echo ERROR: test directory not found!Please run from project root.
    exit /b 1
)

REM Check if pytest is installed
python -c "import pytest" 2>nul
if errorlevel 1 (
    echo Installing missing pytest...
    pip install -r test\requirements-test.txt
)

REM Run the tests
echo.
echo Running tests...
echo.

REM Run all tests
pytest test\ ^
    --tb=short ^
    --color=yes ^
    -v

echo.
echo ==========================================
echo All tests completed!
echo ==========================================

pause