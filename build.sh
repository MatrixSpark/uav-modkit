#!/bin/bash
# UAV ModKit ROS 2 Build Script
# This script builds all ROS 2 packages in the workspace

set -e  # Exit on error

echo "=========================================="
echo "UAV ModKit version 0.1.0"
echo "ROS 2 Build Script"
echo "=========================================="

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if ROS 2 is sourced
if [ -z "$ROS_DISTRO" ]; then
    echo "ERROR: ROS 2 is not sourced!"
    echo "Please run: source /opt/ros/humble/setup.bash"
    exit 1
fi

echo "ROS 2 Distribution: $ROS_DISTRO"

# Build the canonical package directories directly.
cd "$SCRIPT_DIR"

echo ""
echo "Installing system dependencies..."
rosdep install --from-paths camera imu lidar power --ignore-src -r -y || true

echo ""
echo "Building packages with colcon..."
colcon build --symlink-install --base-paths camera imu lidar power --event-handlers console_direct+

echo ""
echo "Sourcing workspace..."
source install/setup.bash

echo ""
echo "=========================================="
echo "Build completed successfully!"
echo "=========================================="
echo ""
echo "To use this workspace in the future, run:"
echo "  source install/setup.bash"
echo ""
echo "To list available packages:"
echo "  ros2 pkg list"
echo ""
echo "To run a sensor node:"
echo "  ros2 launch imu_sensor imu_auto.launch.py"
echo ""
