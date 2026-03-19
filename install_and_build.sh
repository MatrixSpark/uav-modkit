#!/bin/bash
# ROS 2 Humble Installation and UAV ModKit Build Script for WSL2/Ubuntu

set -e

echo "=========================================="
echo "ROS 2 Humble Installation for WSL2/Ubuntu"
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
# Add the ROS 2 GPG key properly
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys F42ED6FBAB17C654
# Add the repository
echo "deb [arch=$(dpkg --print-architecture)] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Update package list after adding ROS 2 repo
sudo apt update

# Install ROS 2 Humble and colcon
echo ""
echo "Step 4: Installing ROS 2 Humble..."
sudo apt install -y ros-humble-desktop

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
if ! grep -q "source /opt/ros/humble/setup.bash" ~/.bashrc; then
    echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
fi

# Source the setup
source /opt/ros/humble/setup.bash

echo ""
echo "=========================================="
echo "✅ ROS 2 Humble Installation Complete!"
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

# Build the project
cd ~/uav-modkit 2>/dev/null || cd /mnt/c/Users/user/Documents/GitHub/uav-modkit

# Create workspace
mkdir -p colcon_ws/src

# Build all packages
colcon build --symlink-install

echo ""
echo "=========================================="
echo "✅ Build Complete!"
echo "=========================================="
echo ""
echo "To use the workspace, run:"
echo "  source ~/colcon_ws/install/setup.bash"
echo ""
echo "Then launch a sensor:"
echo "  ros2 launch imu_sensor imu_auto.launch.py"
echo ""
