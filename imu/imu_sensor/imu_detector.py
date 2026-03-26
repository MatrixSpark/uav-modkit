import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class ImuDetector(Node):
    def __init__(self):
        super().__init__('imu_detector')
        self.detected_pub = self.create_publisher(String, '/imu/detected_vendor', 10)
        self.timer = self.create_timer(1.0, self.detect_cb)

    def detect_cb(self):
        # TODO: replace with real detection logic
        # e.g. scan I2C bus, check /dev/tty*, read udev tags, etc.
        detected = 'bosch_bno055'
        msg = String()
        msg.data = detected
        self.detected_pub.publish(msg)
        self.get_logger().info(f'Detected IMU: {detected}')
        # Stop after first detection
        self.timer.cancel()

def main(args=None):
    rclpy.init(args=args)
    node = ImuDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
