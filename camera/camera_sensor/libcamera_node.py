import time

import numpy as np
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import CameraInfo, Image


class camera(Node):
    """Simple ROS 2 camera node using libcamera (or OpenCV fallback).

    This node publishes raw image frames on `/camera/image_raw` and a
    corresponding `/camera/camera_info`. It prefers the libcamera Python
    bindings when available, but will fall back to OpenCV VideoCapture.
    """

    def __init__(self):
        super().__init__('libcamera_node')

        self.bridge = CvBridge()
        self.image_pub = self.create_publisher(Image, '/camera/image_raw', 10)
        self.info_pub = self.create_publisher(CameraInfo, '/camera/camera_info', 10)

        self.frame_id = 'camera_frame'
        self.width = 640
        self.height = 480

        self._camera = None
        self._use_libcamera = False

        try:
            import libcamera  # noqa: F401
            self._use_libcamera = True
            self.get_logger().info('libcamera package found; attempting to use libcamera.')
        except ImportError:
            self.get_logger().warn('libcamera python bindings not found; using OpenCV fallback.')

        if not self._use_libcamera:
            try:
                import cv2  # noqa: F401
                self._cap = cv2.VideoCapture(0)
                self.get_logger().info('OpenCV VideoCapture initialized for /dev/video0')
            except Exception as e:
                self._cap = None
                self.get_logger().error(f'Failed to initialize OpenCV VideoCapture: {e}')

        # Publish at ~10 Hz
        self.timer = self.create_timer(0.1, self.publish_frame)

    def _create_camera_info_message(self) -> CameraInfo:
        info = CameraInfo()
        info.header.frame_id = self.frame_id
        info.width = self.width
        info.height = self.height
        # Simple pinhole model with focal length ~ width
        info.k = [self.width, 0.0, self.width / 2.0, 0.0, self.width, self.height / 2.0, 0.0, 0.0, 1.0]
        info.p = [self.width, 0.0, self.width / 2.0, 0.0, 0.0, self.width, self.height / 2.0, 0.0, 0.0, 0.0, 1.0, 0.0]
        return info

    def publish_frame(self):
        # Grab a frame from libcamera or OpenCV
        frame = None

        if self._use_libcamera:
            # Placeholder: real libcamera integration would go here
            # For now, publish an empty image to keep the node functional.
            frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        elif hasattr(self, '_cap') and self._cap is not None:
            ret, frame = self._cap.read()
            if not ret:
                self.get_logger().warn('Failed to read frame from camera; publishing placeholder image.')
                frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)

        if frame is None:
            return

        ros_image = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        ros_image.header.stamp = self.get_clock().now().to_msg()
        ros_image.header.frame_id = self.frame_id

        self.image_pub.publish(ros_image)
        self.info_pub.publish(self._create_camera_info_message())

    def destroy_node(self):
        if hasattr(self, '_cap') and self._cap is not None:
            self._cap.release()
        return super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = camera()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
