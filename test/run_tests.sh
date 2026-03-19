#!/bin/bash
# UAV ModKit Test Runner
# This script runs all unit tests for the UAV ModKit project

set -e

echo "=========================================="
echo "UAV ModKit - Test Runner"
echo "=========================================="

# Check if we're in the right directory
if [ ! -d "test" ]; then
    echo "ERROR: test directory not found. Please run from project root."
    exit 1
fi

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "Installing pytest..."
    pip install -r test/requirements-test.txt
fi

# Run the tests
echo ""
echo "Running tests..."
echo ""

# Run all tests with coverage
pytest test/ \
    --tb=short \
    --color=yes \
    -v

echo ""
echo "=========================================="
echo "All tests completed!"
echo "=========================================="