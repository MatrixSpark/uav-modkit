from .core import rclpy, Node, String


class IMUInterface(Node):
    def __init__(self, node_name: str, vendor_name: str):
        super(IMUInterface).__init__(node_name)
        self.vendor_name = vendor_name

        # Unified IMU topics
        self.imu_pub = self.create_publisher(Imu, '/imu/data', 10)
        self.status_pub = self.create_publisher(String, '/imu/status', 10)

    def publish_imu(self, msg: Imu):
        self.imu_pub.publish(msg)

    def publish_status(self, text: str):
        s = String()
        s.data = f'{self.vendor_name}: {text}'
        self.status_pub.publish(s)
