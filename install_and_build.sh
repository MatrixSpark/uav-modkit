#!/bin/bash
# ROS 2 Jazzy Installation and UAV ModKit Build Script for WSL2/Ubuntu

set -e

echo "=========================================="
echo "ROS 2 Jazzy Installation for WSL2/Ubuntu"
echo "=========================================="
echo ""

# Update system
echo "Step 1: Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Install basic dependencies
echo ""
echo "Step 2: Installing basic dependencies..."
sudo apt install -y \
  curl \
  gnupg \
  lsb-release

# Add ROS 2 repository
echo ""
echo "Step 3: Adding ROS 2 repository..."
# Import the ROS 2 GPG key into a keyring (modern apt requires signed-by)
echo "Adding ROS 2 GPG key to /usr/share/keyrings/ros-archive-keyring.gpg..."
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo gpg --dearmor -o /usr/share/keyrings/ros-archive-keyring.gpg

# Configure the ROS 2 apt repository using the signed-by mechanism
sudo sh -c 'echo "deb [arch=amd64,arm64 signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/ros2-latest.list'

# Update package list after adding ROS 2 repo
sudo apt update

# Install ROS 2 Jazzy and colcon
echo ""
echo "Step 4: Installing ROS 2 Jazzy..."
sudo apt install -y ros-jazzy-desktop

# Install colcon after ROS 2 repo is added
echo ""
echo "Step 4b: Installing build tools..."
sudo apt install -y python3-colcon-common-extensions python3-pip

# Initialize rosdep
echo ""
echo "Step 5: Initializing rosdep..."
sudo rosdep init
rosdep update

# Add to bashrc
echo ""
echo "Step 6: Setting up shell configuration..."
if ! grep -q "source /opt/ros/jazzy/setup.bash" ~/.bashrc; then
    echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
fi

# Source the setup
source /opt/ros/jazzy/setup.bash

echo ""
echo "=========================================="
echo "✅ ROS 2 Jazzy Installation Complete!"
echo "=========================================="
echo ""

# Verify installation
echo "Verifying ROS 2 installation..."
ros2 --version

echo ""
echo "=========================================="
echo "Building UAV ModKit..."
echo "=========================================="
echo ""

# Build the project from the repository root
cd "$(dirname "${BASH_SOURCE[0]}")"

# Build all packages in-place
colcon build --symlink-install

echo ""
echo "=========================================="
echo "✅ Build Complete!"
echo "=========================================="
echo ""
echo "To use the workspace, source the build output:"
echo "  source install/setup.bash"
echo ""
echo "Then launch a sensor:"
echo "  ros2 launch imu_sensor imu_auto.launch.py"
echo ""
