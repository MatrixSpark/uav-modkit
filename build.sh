#!/bin/bash
# UAV ModKit ROS 2 Build Script
# This script builds all ROS 2 packages in the workspace

set -e  # Exit on error

echo "=========================================="
echo "UAV ModKit - ROS 2 Build Script"
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

# Create colcon workspace structure
echo "Creating workspace structure..."
mkdir -p colcon_ws/src

# Copy packages (if in a Git repo)
if [ -d ".git" ]; then
    echo "Copying packages to colcon workspace..."
    cp -r imu colcon_ws/src/imu_sensor || true
    cp -r lidar colcon_ws/src/lidar_sensor || true
    cp -r power colcon_ws/src/power_mgr || true
fi

cd colcon_ws

# Install dependencies
echo ""
echo "Installing system dependencies..."
rosdep install --from-paths src --ignore-src -r -y || true

# Build
echo ""
echo "Building packages with colcon..."
colcon build --symlink-install --event-handlers console_direct+

# Source the newly built workspace
echo ""
echo "Sourcing workspace..."
source install/setup.bash

echo ""
echo "=========================================="
echo "Build completed successfully!"
echo "=========================================="
echo ""
echo "To use this workspace in the future, run:"
echo "  source ~/colcon_ws/install/setup.bash"
echo ""
echo "To list available packages:"
echo "  ros2 pkg list"
echo ""
echo "To run a sensor node:"
echo "  ros2 launch imu_sensor imu_auto.launch.py"
echo ""
