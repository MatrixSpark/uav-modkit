import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu


class BoschBNO055Imu(Node):
	def __init__(self):
		super().__init__('bosch_bno055_imu_node')
		self.publisher = self.create_publisher(Imu, '/imu/data', 10)
		# Publish sample data at 50 Hz; replace with hardware readout when available.
		self.timer = self.create_timer(0.02, self.publish_imu)

	def publish_imu(self):
		msg = Imu()
		msg.header.stamp = self.get_clock().now().to_msg()
		msg.header.frame_id = 'imu_link'
		msg.orientation_covariance[0] = -1.0
		msg.angular_velocity_covariance[0] = -1.0
		msg.linear_acceleration_covariance[0] = -1.0
		self.publisher.publish(msg)


def main(args=None):
	rclpy.init(args=args)
	node = BoschBNO055Imu()
	rclpy.spin(node)
	node.destroy_node()
	rclpy.shutdown()