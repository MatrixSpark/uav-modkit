import os

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class CameraDetector(Node):
    """Detects whether a compatible camera is available on the system.

    This is a simple heuristic that checks for a connected video device.
    It also serves as a placeholder for more advanced detection logic (e.g.
    using libcamera's CameraManager).
    """

    def __init__(self):
        super().__init__('camera_detector')
        self.detected_pub = self.create_publisher(String, '/camera/detected_vendor', 10)
        self.timer = self.create_timer(1.0, self.detect_cb)

    def detect_cb(self):
        # Default vendor name for demonstration purposes
        detected = 'libcamera' if self._has_video_device() else 'none'

        msg = String()
        msg.data = detected
        self.detected_pub.publish(msg)
        self.get_logger().info(f'Detected camera vendor: {detected}')

        # Only run once for now
        self.timer.cancel()

    def _has_video_device(self) -> bool:
        # Common video device on Linux
        return os.path.exists('/dev/video0')


def main(args=None):
    rclpy.init(args=args)
    node = CameraDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
