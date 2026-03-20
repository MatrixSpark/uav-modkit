import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class LidarDetector(Node):
    def __init__(self):
        super().__init__('lidar_detector')
        self.detected_pub = self.create_publisher(String, '/lidar/detected_vendor', 10)
        self.timer = self.create_timer(1.0, self.detect_cb)

    def detect_cb(self):
        # TODO: replace with real detection logic
        # e.g. check /dev/ttyUSB*, ping IPs, read udev tags, etc.
        detected = 'velodyne'  # 'velodyne'
        msg = String()
        msg.data = detected
        self.detected_pub.publish(msg)
        self.get_logger().info(f'Detected LiDAR: {detected}')
        # Could stop timer after first detection
        self.timer.cancel()

def main(args=None):
    rclpy.init(args=args)
    node = LidarDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
