import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class DeployManager(Node):
    def __init__(self):
        super().__init__('deployment_manager')

        self.imu_vendor = "bosch"
        self.lidar_vendor = "velodyne"
        self.gps_vendor = " novatel"

        # Swap state tracking
        self.swap_in_progress = False
        self.swap_target_sensor = None
        self.swap_target_vendor = None
        self.supported_imu_vendors = ["bosch", "xsens", "vn310"]
        self.supported_lidar_vendors = ["velodyne", "riegl", "vulcan", "harris"]

        # Subscriptions
        self.create_subscription(String, '/imu/detected_vendor', self.imu_cb, 10)
        self.create_subscription(String, '/lidar/detected_vendor', self.lidar_cb, 10)
        self.create_subscription(String, '/sensors/health', self.health_cb, 10)
        self.create_subscription(String, '/system/swap_command', self.swap_cb, 10)

        # Publishers
        self.status_pub = self.create_publisher(String, '/system/status', 10)
        self.swap_status_pub = self.create_publisher(String, '/system/swap_status', 10)

        # Internal health state
        self.health_state = "unknown"

        # Periodic system status broadcast
        self.timer = self.create_timer(1.0, self.publish_status)

    def imu_cb(self, msg):
        self.imu_vendor = msg.data
        self.get_logger().info(f"IMU detected: {self.imu_vendor}")

    def lidar_cb(self, msg):
        self.lidar_vendor = msg.data
        self.get_logger().info(f"LiDAR detected: {self.lidar_vendor}")

    def health_cb(self, msg):
        self.health_state = msg.data

    def swap_cb(self, msg):
        """Handle swap commands from topic /system/swap_command
        
        Format: "SWAP <sensor_type> <target_vendor>"
        Example: "SWAP IMU xsens" or "SWAP LIDAR riegl"
        """
        command_parts = msg.data.split()
        
        if len(command_parts) < 3 or command_parts[0] != "SWAP":
            self.get_logger().warn(f"Invalid swap command: {msg.data}")
            return
        
        sensor_type = command_parts[1].upper()
        target_vendor = command_parts[2].lower()
        
        self.execute_swap(sensor_type, target_vendor)

    def execute_swap(self, sensor_type, target_vendor):
        """Execute swap for a specific sensor type and vendor"""
        if self.swap_in_progress:
            self.get_logger().warn("Swap already in progress")
            self.publish_swap_status(f"FAILED: Swap already in progress")
            return
        
        # Validate sensor type
        if sensor_type == "IMU":
            if target_vendor not in self.supported_imu_vendors:
                self.get_logger().warn(f"Unsupported IMU vendor: {target_vendor}")
                self.publish_swap_status(f"FAILED: Unsupported IMU vendor {target_vendor}")
                return
            self.perform_imu_swap(target_vendor)
        
        elif sensor_type == "LIDAR":
            if target_vendor not in self.supported_lidar_vendors:
                self.get_logger().warn(f"Unsupported LiDAR vendor: {target_vendor}")
                self.publish_swap_status(f"FAILED: Unsupported LiDAR vendor {target_vendor}")
                return
            self.perform_lidar_swap(target_vendor)
        
        else:
            self.get_logger().warn(f"Unknown sensor type: {sensor_type}")
            self.publish_swap_status(f"FAILED: Unknown sensor type {sensor_type}")

    def perform_imu_swap(self, target_vendor):
        """Perform IMU swap to target vendor"""
        self.swap_in_progress = True
        self.swap_target_sensor = "IMU"
        self.swap_target_vendor = target_vendor
        
        self.get_logger().info(f"Starting IMU swap from {self.imu_vendor} to {target_vendor}")
        self.publish_swap_status(f"IN_PROGRESS: Swapping IMU from {self.imu_vendor} to {target_vendor}")
        
        old_vendor = self.imu_vendor
        self.imu_vendor = target_vendor
        
        self.get_logger().info(f"IMU swap completed: {old_vendor} -> {target_vendor}")
        self.publish_swap_status(f"SUCCESS: IMU swapped from {old_vendor} to {target_vendor}")
        
        self.swap_in_progress = False

    def perform_lidar_swap(self, target_vendor):
        """Perform LiDAR swap to target vendor"""
        self.swap_in_progress = True
        self.swap_target_sensor = "LIDAR"
        self.swap_target_vendor = target_vendor
        
        self.get_logger().info(f"Starting LiDAR swap from {self.lidar_vendor} to {target_vendor}")
        self.publish_swap_status(f"IN_PROGRESS: Swapping LiDAR from {self.lidar_vendor} to {target_vendor}")
        
        old_vendor = self.lidar_vendor
        self.lidar_vendor = target_vendor
        
        self.get_logger().info(f"LiDAR swap completed: {old_vendor} -> {target_vendor}")
        self.publish_swap_status(f"SUCCESS: LiDAR swapped from {old_vendor} to {target_vendor}")
        
        self.swap_in_progress = False

    def publish_swap_status(self, status_message):
        """Publish swap status update"""
        msg = String()
        msg.data = status_message
        self.swap_status_pub.publish(msg)
        self.get_logger().info(f"Swap Status: {status_message}")

    def publish_status(self):
        msg = String()
        swap_info = f" | Swap: {'IN_PROGRESS' if self.swap_in_progress else 'READY'}"
        msg.data = (
            f"IMU={self.imu_vendor} | "
            f"LiDAR={self.lidar_vendor} | "
            f"Health={self.health_state}"
            f"{swap_info}"
        )
        self.status_pub.publish(msg)
        self.get_logger().info(f"System Status: {msg.data}")

def main(args=None):
    rclpy.init(args=args)
    node = DeployManager()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
