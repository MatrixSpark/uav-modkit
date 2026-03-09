import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from std_msgs.msg import String

class ImuPayloadAdapter(Node):
    def __init__(self):
        super().__init__('imu_payload_adapter')

        self.vendor = "unknown"

        # Which IMU is active
        self.create_subscription(
            String,
            '/imu/detected_vendor',
            self.vendor_cb,
            10
        )

        # Raw IMU data
        self.create_subscription(
            Imu,
            '/imu/data',
            self.imu_cb,
            10
        )

        # Payload‑level status (for higher‑level systems)
        self.status_pub = self.create_publisher(String, '/payload/imu_status', 10)

    def vendor_cb(self, msg: String):
        self.vendor = msg.data
        self.get_logger().info(f"Active IMU vendor: {self.vendor}")

    def imu_cb(self, msg: Imu):
        # Here you could downsample, transform frames, or compute quality metrics
        status = String()
        status.data = f"IMU={self.vendor} | seq={msg.header.stamp.sec}"
        self.status_pub.publish(status)

def main(args=None):
    rclpy.init(args=args)
    node = ImuPayloadAdapter()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
