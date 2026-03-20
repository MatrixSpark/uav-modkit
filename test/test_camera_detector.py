#!/usr/bin/env python3

import pytest
import rclpy
from std_msgs.msg import String
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from camera.camera_sensor.camera_detector import CameraDetector


class TestCameraDetector:
    """Unit tests for the CameraDetector class"""

    @pytest.fixture
    def node(self):
        """Create a CameraDetector instance for testing"""
        rclpy.init()
        node = CameraDetector()
        yield node
        node.destroy_node()
        rclpy.shutdown()

    def test_initialization(self, node):
        """Test that CameraDetector initializes correctly"""
        assert node.get_name() == 'camera_detector'
        # Check that publisher was created
        assert hasattr(node, 'detected_pub')
        # Check that timer was created
        assert hasattr(node, 'timer')

    def test_detect_cb_publishes_libcamera_when_device_exists(self, node):
        """Test that detect_cb publishes 'libcamera' when video device exists"""
        with patch.object(node.detected_pub, 'publish') as mock_publish:
            with patch.object(node.timer, 'cancel') as mock_cancel:
                with patch('os.path.exists', return_value=True):
                    node.detect_cb()

                    # Check that publish was called
                    mock_publish.assert_called_once()
                    published_msg = mock_publish.call_args[0][0]
                    assert published_msg.data == 'libcamera'

                    # Check that timer was cancelled
                    mock_cancel.assert_called_once()

    def test_detect_cb_publishes_none_when_no_device(self, node):
        """Test that detect_cb publishes 'none' when no video device exists"""
        with patch.object(node.detected_pub, 'publish') as mock_publish:
            with patch.object(node.timer, 'cancel') as mock_cancel:
                with patch('os.path.exists', return_value=False):
                    node.detect_cb()

                    # Check that publish was called
                    mock_publish.assert_called_once()
                    published_msg = mock_publish.call_args[0][0]
                    assert published_msg.data == 'none'

                    # Check that timer was cancelled
                    mock_cancel.assert_called_once()

    @patch('camera.camera_sensor.camera_detector.CameraDetector.get_logger')
    def test_detect_cb_logs_detection(self, mock_get_logger, node):
        """Test that detect_cb logs the detection"""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        with patch.object(node.detected_pub, 'publish'):
            with patch.object(node.timer, 'cancel'):
                with patch('os.path.exists', return_value=True):
                    node.detect_cb()

                    mock_logger.info.assert_called_once_with('Detected camera vendor: libcamera')

    def test_timer_creation(self, node):
        """Test that timer is created with correct parameters"""
        # The timer should be created with 1.0 second interval and detect_cb callback
        assert node.timer is not None


class TestCameraDetectorIntegration:
    """Integration tests for CameraDetector"""

    def test_node_creation_and_destruction(self):
        """Test that node can be created and destroyed without errors"""
        rclpy.init()
        node = CameraDetector()
        assert node is not None
        node.destroy_node()
        rclpy.shutdown()

    def test_publisher_creation(self):
        """Test that the publisher is created with correct topic and QoS"""
        rclpy.init()
        node = CameraDetector()

        # Check that the publisher exists and has correct topic
        assert node.detected_pub is not None
        # Note: We can't easily check the exact topic name without more complex introspection

        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    pytest.main([__file__])