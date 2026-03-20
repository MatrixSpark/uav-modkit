# 🛩️ UAV ModKit

## A Modular Platform for UAVs

UAV ModKit is an open-source ROS 2 framework that enables runtime-swappable sensors and payloads for unmanned aerial vehicles. This project provides a clean, extensible architecture for detecting, loading, and managing sensor modules on the fly, including IMU, LiDAR, Camera, power management, and health monitoring systems.

## Who Is This For?

UAV ModKit is designed for a wide range of UAV builders — from enthusiastic hobbyists exploring modular drone design to researchers and engineers developing advanced multi-mission platforms. The idea is to keep things simple for beginners while remaining powerful and extensible for experienced ROS 2 developers. Whether you're experimenting with swappable sensors at home or building a professional UAV system, UAV ModKit gives you a complete kit to work from.

## ✨ Features

🔌 **Runtime Sensor Swap**  
Detect, attach, and activate new sensor modules without rebooting the UAV.

🧩 **Modular ROS 2 Package Structure**  
Each sensor is a self-contained ROS 2 component with its own package.xml, drivers, topics, and resources. Uses ament_python for ROS 2 packages.

📦 **Deployment Manager Node**  
Handles discovery, initialization, and runtime swapping of sensors.

🔄 **Dynamic Launcher **  
Automatically starts and stops sensor-specific nodes based on what's physically connected.

📷 **Camera Support**  
Integrated camera sensor support using libcamera with ROS 2 image transport, including automatic detection and payload processing.

## 🚀 Dynamic Launcher 

UAV ModKit uses ROS 2 launch files and the deployment manager to dynamically orchestrate sensor nodes based on detected hardware.

### Launcher Example (`launch/imu_auto.launch.py`)

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launcher():
    # Detector node identifies the IMU which is physically present
    detector = Node(
        package='imu',
        executable='imu_detector',
        name='imu_detector',
        output='screen'
    )

    # Bosch BNO055 IMU driver
    bosch_bno055 = Node(
        package='imu',
        executable='bosch_bno055_imu',
        name='bosch_bno055_imu_node',
        output='screen',
        parameters=[{
            'vendor': 'bosch_bno055',
            'enabled': False   # controlled by deployment manager
        }]
    )

    # Payload adapter for data processing
    payload_adapter = Node(
        package='imu',
        executable='imu_payload_adapter',
        name='imu_payload_adapter',
        output='screen'
    )

    return LaunchDescription([
        detector,
        bosch_bno055,
        payload_adapter
    ])
```

### Sensor Swapping

The deployment manager enables runtime sensor swapping through ROS 2 topics. Send commands to `/system/swap_command` to dynamically change sensor configurations.

### Sensor Detection 

Sensor detectors automatically identify connected hardware and publish vendor information to enable dynamic configuration.

### Usage Examples

```bash
# Launch IMU sensor suite
ros2 launch imu_sensor imu_auto.launch.py

# Launch LiDAR sensor suite
ros2 launch lidar_sensor lidar_auto.launch.py

# Launch Camera sensor suite
ros2 launch camera_sensor camera_auto.launch.py

# Swap IMU sensor at runtime
ros2 topic pub /system/swap_command std_msgs/msg/String "data: 'SWAP IMU xsens'"

# Swap LiDAR sensor at runtime
ros2 topic pub /system/swap_command std_msgs/msg/String "data: 'SWAP LIDAR riegl'"

# Swap Camera sensor at runtime (example)
ros2 topic pub /system/swap_command std_msgs/msg/String "data: 'SWAP CAMERA libcamera'"

# Monitor system status
ros2 topic echo /system/status

# Monitor swap operations
ros2 topic echo /system/swap_status
```

🛡️ **Health & Status Monitoring**  
Integrates with system-level health checks to ensure safe operation during sensor swaps.

🧱 **Extensible Plugin Architecture**  
Add new sensor types by dropping in a module — no core code changes required.

## 📁 Project Structure

```
uav-modkit/
├── .colcon/                    # Colcon build configuration
├── core/                       # Core functionality
│   └── core.py
├── deploy/                     # Deployment manager with swap capabilities
│   └── Deploy.py
├── imu/                        # IMU sensor package
│   ├── imu_params.yaml         # IMU configuration parameters
│   ├── imu_sensor/             # IMU sensor implementations
│   ├── package.xml
│   ├── resource/
│   └── setup.py
├── launch/                     # Launch files for all sensors
├── lidar/                      # LiDAR sensor package
│   ├── detector.py             # LiDAR detection logic
│   ├── package.xml
│   ├── payload_mgr.py          # Payload management
│   ├── resource/
│   ├── setup.py
│   ├── velodyne.py             # Velodyne driver
│   └── __init__.py
├── camera/                     # Camera sensor package
│   ├── package.xml
│   ├── resource/
│   ├── setup.py
│   └── camera_sensor/          # Camera sensor implementation (libcamera)
├── monitor/                    # Health monitoring
│   ├── battery.py              # Battery monitoring
│   └── sensor_health.py        # Sensor health checks
├── power/                      # Power management package
│   ├── package.xml
│   ├── resource/
│   └── setup.py
├── test/                      # Unit tests and test configuration
│   ├── test_deploy_manager.py    # DeployManager tests
│   ├── test_lidar_detector.py    # LiDAR detector tests
│   ├── test_imu_detector.py      # IMU detector tests
│   ├── test_camera_detector.py   # Camera detector tests
│   ├── test_integration.py       # Integration tests
│   ├── pytest.ini               # Pytest configuration
│   ├── requirements-test.txt    # Test dependencies
│   ├── run_tests.sh             # Linux test runner
│   └── run_tests.bat            # Windows test runner
```

## 🚀 Getting Started

### 1. Prerequisites
- **ROS 2 Humble** (recommended) or Iron
- Python 3.10+
- A UAV platform running ROS 2 (PX4, ArduPilot, or custom)

### Installing ROS 2 (Humble / Jazzy)

UAV ModKit is developed against ROS 2 Humble (Ubuntu 22.04) and also supports ROS 2 Jazzy (Ubuntu 24.04). Use the version that matches your Ubuntu release:

- **Ubuntu 22.04 (Jammy)** → ROS 2 Humble (recommended)
- **Ubuntu 24.04 (Noble)** → ROS 2 Jazzy (newer; may require extra TLS/keyring steps)

#### Ubuntu / WSL2 (recommended)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y curl gnupg lsb-release ca-certificates

# Configure the ROS 2 apt repository (modern keyring method)
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc \
  | sudo gpg --dearmor -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=amd64,arm64 signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
  http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" \
  | sudo tee /etc/apt/sources.list.d/ros2.list

# Install ROS 2 (choose Humble or Jazzy based on your Ubuntu version)
sudo apt update
sudo apt install -y ros-humble-desktop  # or ros-jazzy-desktop on Ubuntu 24.04

# Add setup to your shell
echo "source /opt/ros/$(lsb_release -cs | sed -e 's/jammy/humble/' -e 's/noble/jazzy/')/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

> ⚠️ If `apt update` fails with a certificate error like `Certificate verification failed: ...`, it may indicate a network proxy / TLS interception or an outdated CA bundle. Try:
>
> ```bash
> curl -v https://packages.ros.org/ros2/ubuntu/dists/$(lsb_release -cs)/InRelease
> sudo apt install --reinstall ca-certificates
> ```

**On Windows (native):**

Download from https://github.com/ros2/ros2/releases and extract to `C:\opt\ros2`.

### 2. Clone the repository
```bash
git clone https://github.com/<your-username>/uav-modkit.git
cd uav-modkit
```

### 3. Build the workspace
```bash
# Option A: Use the automated script (recommended)
./install_and_build.sh

# Option B: Manual build
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
```

### 4. Launch sensors
```bash
# Launch IMU sensor
ros2 launch imu_sensor imu_auto.launch.py

# Launch LiDAR sensor
ros2 launch lidar_sensor lidar_auto.launch.py

# Launch Camera sensor
ros2 launch camera_sensor camera_auto.launch.py

# Launch power manager
ros2 launch power_mgr power_auto.launch.py
```

### 5. Monitor system status
```bash
# View all topics
ros2 topic list

# Monitor system status
ros2 topic echo /system/status

# Monitor sensor data
ros2 topic echo /imu/data
ros2 topic echo /lidar/scan
ros2 topic echo /camera/image_raw
```

## 🔄 Runtime Sensor Swapping

UAV ModKit supports runtime sensor swapping through the deployment manager:

```bash
# Swap IMU sensor
ros2 topic pub /system/swap_command std_msgs/msg/String "data: 'SWAP IMU xsens'"

# Swap LiDAR sensor
ros2 topic pub /system/swap_command std_msgs/msg/String "data: 'SWAP LIDAR riegl'"

# Swap Camera sensor
ros2 topic pub /system/swap_command std_msgs/msg/String "data: 'SWAP CAMERA opencv'"

# Monitor swap status
ros2 topic echo /system/swap_status
```

Supported sensors:
- **IMU:** bosch, xsens, vn310
- **LiDAR:** velodyne, riegl, vulcan, harris
- **Camera:** libcamera, opencv

## 🛠️ Creating Custom Sensors

1. Create a new directory under the project root (e.g., `custom_sensor/`)
2. Add `package.xml` and `setup.py` files
3. Implement sor driver
4. Add launch files in the `launch/` directory
5. Update the deployment manager to support your sensor

See the existing sensor packages (imu/, lidar/, power/) for examples.

## � Testing

UAV ModKit includes a comprehensive test suite to ensure code quality and reliability.

### Running Tests

```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
./test/run_tests.sh              # Linux/WSL2
test\run_tests.bat               # Windows

# Or run tests directly with pytest
pytest test/ -v
```

### Test Coverage

The test suite includes:
- **Unit tests** for individual components (DeployManager, IMU/LiDAR/Camera detectors)
- **Integration tests** for system-wide functionality
- **Mock-based testing** for ROS 2 components

### Writing Tests

Tests are located in the `test/` directory. Use pytest fixtures and mocking for ROS 2 components:

```python
import pytest
from unittest.mock import patch

def test_my_function(node):
    with patch.object(node.publisher, 'publish') as mock_publish:
        # Test code here
        pass
```

## �🤝 Contributing

Contributions are welcome — whether it's new sensor modules, bug fixes, or improvements to the deployment manager. Please open an issue or submit a pull request.

## 📄 License

This project is licensed under the Apache 2.0 License, the same license used by ROS 2. It provides strong protection while encouraging open collaboration.
