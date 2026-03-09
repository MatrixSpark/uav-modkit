import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class DeployManager(Node):
    def __init__(self):
        super().__init__('deployment_manager')

        self.imu_vendor = "bosch"
        self.lidar_vendor = "velodyne"
        self.gps_vendor = " novatel"

        # Subscriptions
        self.create_subscription(String, '/imu/detected_vendor', self.imu_cb, 10)
        self.create_subscription(String, '/lidar/detected_vendor', self.lidar_cb, 10)
        self.create_subscription(String, '/sensors/health', self.health_cb, 10)

        # Unified system status
        self.status_pub = self.create_publisher(String, '/system/status', 10)

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

    def publish_status(self):
        msg = String()
        msg.data = (
            f"IMU={self.imu_vendor} | "
            f"LiDAR={self.lidar_vendor} | "
            f"Health={self.health_state}"
        )
        self.status_pub.publish(msg)
        self.get_logger().info(f"System Status: {msg.data}")

def main(args=None):
    rclpy.init(args=args)
    node = DeploymentManager()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
