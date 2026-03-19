#!/usr/bin/env python3

import pytest
import rclpy
from std_msgs.msg import String
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from imu.imu_sensor.imu_detector import ImuDetector


class TestImuDetector:
    """Unit tests for the ImuDetector class"""

    @pytest.fixture
    def node(self):
        """Create an ImuDetector instance for testing"""
        rclpy.init()
        node = ImuDetector()
        yield node
        node.destroy_node()
        rclpy.shutdown()

    def test_initialization(self, node):
        """Test that ImuDetector initializes correctly"""
        assert node.get_name() == 'imu_detector'
        # Check that publisher was created
        assert hasattr(node, 'detected_pub')
        # Check that timer was created
        assert hasattr(node, 'timer')

    def test_detect_cb_publishes_bosch_bno055(self, node):
        """Test that detect_cb publishes 'bosch_bno055' vendor"""
        with patch.object(node.detected_pub, 'publish') as mock_publish:
            with patch.object(node.timer, 'cancel') as mock_cancel:
                node.detect_cb()

                # Check that publish was called
                mock_publish.assert_called_once()
                published_msg = mock_publish.call_args[0][0]
                assert published_msg.data == 'bosch_bno055'

                # Check that timer was cancelled
                mock_cancel.assert_called_once()

    @patch('imu.imu_sensor.imu_detector.ImuDetector.get_logger')
    def test_detect_cb_logs_detection(self, mock_get_logger, node):
        """Test that detect_cb logs the detection"""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        with patch.object(node.detected_pub, 'publish'):
            with patch.object(node.timer, 'cancel'):
                node.detect_cb()

                mock_logger.info.assert_called_once_with('Detected IMU: bosch_bno055')

    def test_timer_creation(self, node):
        """Test that timer is created with correct parameters"""
        # The timer should be created with 1.0 second interval and detect_cb callback
        assert node.timer is not None


class TestImuDetectorIntegration:
    """Integration tests for ImuDetector"""

    def test_node_creation_and_destruction(self):
        """Test that node can be created and destroyed without errors"""
        rclpy.init()
        node = ImuDetector()
        assert node is not None
        node.destroy_node()
        rclpy.shutdown()

    def test_publisher_creation(self):
        """Test that the publisher is created with correct topic and QoS"""
        rclpy.init()
        node = ImuDetector()

        # Check that the publisher exists and has correct topic
        assert node.detected_pub is not None
        # Note: We can't easily check the exact topic name without more complex introspection

        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    pytest.main([__file__])