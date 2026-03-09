 🛩️ uav-modkit
 ## A Modern, Modular, Reconfigurable platform based on ROS 2‑Enabled UAVs
uav-modkit is an open‑source ROS 2 framework that enables runtime‑swappable payloads for unmanned aerial vehicles.Some application include cameras, LiDAR, environmental sensors, or other mission‑specific tools. This project provides a clean, extensible architecture for detecting, loading, and managing payload modules on the fly 

## Who Is This For?

uav-modkit is designed for a wide range of UAV builders — from enthusiastic hobbyists exploring modular drone design to researchers and engineers developing advanced multi‑mission platforms. The idea is to keeps things simple for beginners while remaining powerful and extensible for experienced ROS 2 developers. Whether you're experimenting with swappable sensors at home or building a professional UAV system, uav-modkit gives you a kit to work from.

✨ Features
🔌 Hot‑swappable payloads  
Detect, attach, and activate new payload modules without rebooting the UAV.

🧩 Modular ROS 2 package structure  
Each payload is a self‑contained ROS 2 component with its own package xml, drivers, topics, and resource. ament_python is required for ROS2 packages

📦 Payload Manager Node  
Handles discovery, initialization, and teardown of payloads at runtime.

🔄 Dynamic launch orchestration  
Automatically starts and stops payload‑specific nodes based on what’s physically connected.

🛡️ Health & status monitoring  
Integrates with system‑level health checks to ensure safe operation during payload swaps.

🧱 Extensible plugin architecture  
Add new payload types by dropping in a module — no core code changes required.

📁 Repo Tree 
````
uav-modkit/
├── payload_manager/        # Core runtime manager for payloads
├── payload_interfaces/     # Common message & service definitions
├── payload_modules/       # Example payload modules (camera, lidar, etc.)
├── docs/                   # Documentation & diagrams
└── launch/                 # Unified bring-up and dynamic launch files
````

🚀 Getting Started
##1. Prerequisites
ROS 2 Humble or Iron
Python 3.10+
A UAV platform running ROS 2 (PX4, ArduPilot, or custom)
##2.Clone the repository
bash
git clone https://github.com/<your-username>/uav-modkit.git
cd uav-modkit
##3. Build the workspace
bash
colcon build --symlink-install
source install/setup.bash
##4. Creating Your Own custom module
Create a new folder under payload_modules/
##5. Implement the required interface from payload_interfaces/
##6. Add your launch file
##7. Add your new module in the payload manager
The system will automatically detect and load it at runtime.

📚 Documentation
Full documentation, architecture diagrams, and payload development guides are available in the docs/ directory.
(You can expand this section as the project grows.)

🤝 Contributing
Contributions are welcome — whether it’s new payload modules, bug fixes, or improvements to the deployment manager.
Please open an issue or submit a pull request.

📄 License
This project is licensed under the Apache 2.0 License, the same license used by ROS 2.
It provides strong protection while encouraging open collaboration.
