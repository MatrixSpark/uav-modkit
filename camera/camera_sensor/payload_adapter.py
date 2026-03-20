import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class CameraPayloadAdapter(Node):
    """Example payload adapter that can be extended for onboard processing."""

    def __init__(self):
        super().__init__('camera_payload_adapter')
        self.status_pub = self.create_publisher(String, '/camera/payload_status', 10)
        self.create_timer(2.0, self.publish_status)

    def publish_status(self):
        msg = String()
        msg.data = 'camera payload active'
        self.status_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = CameraPayloadAdapter()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
