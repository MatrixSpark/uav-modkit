import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from std_msgs.msg import String

from lidar_sensor.common_interface import UnifiedLidarPublisher
from lidar_sensor.velodyne_protocol import VelodyneClient

class VelodyneLidarNode(UnifiedLidarPublisher):
    def __init__(self):
        super().__init__('velodyne_lidar_node', 'velodyne')

        self.declare_parameter('enabled', False)
        self.enabled = self.get_parameter('enabled').value

        # Subscribe to detector output
        self.create_subscription(
            String,
            '/lidar/detected_vendor',
            self.vendor_cb,
            10
        )

        # Velodyne UDP client
        self.client = VelodyneClient()
        self.client.connect()

        # Polling loop (10 Hz default)
        self.timer = self.create_timer(0.1, self.poll_cb)

    def vendor_cb(self, msg: String):
        self.enabled = (msg.data == 'velodyne')

    def poll_cb(self):
        if not self.enabled:
            return

        packet = self.client.receive_packet()
        if packet is None:
            return

        # TODO: parse Velodyne packet → PointCloud2
        cloud = PointCloud2()
        self.publish_points(cloud)
        self.publish_status("OK")

    def destroy_node(self):
        self.client.close()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = VelodyneLidarNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
