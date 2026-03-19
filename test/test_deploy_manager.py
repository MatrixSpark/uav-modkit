#!/usr/bin/env python3

import pytest
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from unittest.mock import MagicMock, patch
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from deploy.Deploy import DeployManager


class TestDeployManager:
    """Unit tests for the DeployManager class"""

    @pytest.fixture
    def node(self):
        """Create a DeployManager instance for testing"""
        rclpy.init()
        node = DeployManager()
        yield node
        node.destroy_node()
        rclpy.shutdown()

    def test_initialization(self, node):
        """Test that DeployManager initializes with correct default values"""
        assert node.imu_vendor == "bosch"
        assert node.lidar_vendor == "velodyne"
        assert node.gps_vendor == " novatel"
        assert node.swap_in_progress == False
        assert node.swap_target_sensor == None
        assert node.swap_target_vendor == None
        assert node.health_state == "unknown"

        # Check supported vendors
        assert "bosch" in node.supported_imu_vendors
        assert "xsens" in node.supported_imu_vendors
        assert "vn310" in node.supported_imu_vendors
        assert "velodyne" in node.supported_lidar_vendors
        assert "riegl" in node.supported_lidar_vendors

    def test_imu_callback(self, node):
        """Test IMU vendor detection callback"""
        msg = String()
        msg.data = "xsens"

        node.imu_cb(msg)

        assert node.imu_vendor == "xsens"

    def test_lidar_callback(self, node):
        """Test LiDAR vendor detection callback"""
        msg = String()
        msg.data = "riegl"

        node.lidar_cb(msg)

        assert node.lidar_vendor == "riegl"

    def test_health_callback(self, node):
        """Test health status callback"""
        msg = String()
        msg.data = "healthy"

        node.health_cb(msg)

        assert node.health_state == "healthy"

    def test_swap_callback_valid_command(self, node):
        """Test swap command callback with valid command"""
        msg = String()
        msg.data = "SWAP IMU xsens"

        with patch.object(node, 'execute_swap') as mock_execute:
            node.swap_cb(msg)
            mock_execute.assert_called_once_with("IMU", "xsens")

    def test_swap_callback_invalid_command(self, node):
        """Test swap command callback with invalid command"""
        msg = String()
        msg.data = "INVALID COMMAND"

        with patch.object(node, 'publish_swap_status') as mock_publish:
            node.swap_cb(msg)
            mock_publish.assert_called_once_with("FAILED: Invalid swap command: INVALID COMMAND")

    def test_execute_swap_imu_valid(self, node):
        """Test executing valid IMU swap"""
        with patch.object(node, 'perform_imu_swap') as mock_perform:
            node.execute_swap("IMU", "xsens")
            mock_perform.assert_called_once_with("xsens")

    def test_execute_swap_imu_invalid_vendor(self, node):
        """Test executing IMU swap with invalid vendor"""
        with patch.object(node, 'publish_swap_status') as mock_publish:
            node.execute_swap("IMU", "invalid_vendor")
            mock_publish.assert_called_once_with("FAILED: Unsupported IMU vendor invalid_vendor")

    def test_execute_swap_lidar_valid(self, node):
        """Test executing valid LiDAR swap"""
        with patch.object(node, 'perform_lidar_swap') as mock_perform:
            node.execute_swap("LIDAR", "riegl")
            mock_perform.assert_called_once_with("riegl")

    def test_execute_swap_lidar_invalid_vendor(self, node):
        """Test executing LiDAR swap with invalid vendor"""
        with patch.object(node, 'publish_swap_status') as mock_publish:
            node.execute_swap("LIDAR", "invalid_vendor")
            mock_publish.assert_called_once_with("FAILED: Unsupported LiDAR vendor invalid_vendor")

    def test_execute_swap_unknown_sensor(self, node):
        """Test executing swap with unknown sensor type"""
        with patch.object(node, 'publish_swap_status') as mock_publish:
            node.execute_swap("UNKNOWN", "some_vendor")
            mock_publish.assert_called_once_with("FAILED: Unknown sensor type UNKNOWN")

    def test_execute_swap_already_in_progress(self, node):
        """Test executing swap when another swap is in progress"""
        node.swap_in_progress = True

        with patch.object(node, 'publish_swap_status') as mock_publish:
            node.execute_swap("IMU", "xsens")
            mock_publish.assert_called_once_with("FAILED: Swap already in progress")

    def test_perform_imu_swap(self, node):
        """Test performing IMU swap"""
        original_vendor = node.imu_vendor

        with patch.object(node, 'publish_swap_status') as mock_publish:
            node.perform_imu_swap("xsens")

            assert node.swap_in_progress == False
            assert node.imu_vendor == "xsens"
            assert mock_publish.call_count == 2  # IN_PROGRESS and SUCCESS messages

    def test_perform_lidar_swap(self, node):
        """Test performing LiDAR swap"""
        original_vendor = node.lidar_vendor

        with patch.object(node, 'publish_swap_status') as mock_publish:
            node.perform_lidar_swap("riegl")

            assert node.swap_in_progress == False
            assert node.lidar_vendor == "riegl"
            assert mock_publish.call_count == 2  # IN_PROGRESS and SUCCESS messages

    def test_publish_swap_status(self, node):
        """Test publishing swap status"""
        with patch.object(node.swap_status_pub, 'publish') as mock_publish:
            node.publish_swap_status("TEST_STATUS")

            mock_publish.assert_called_once()
            assert mock_publish.call_args[0][0].data == "TEST_STATUS"

    def test_publish_status_includes_swap_info(self, node):
        """Test that publish_status includes swap information"""
        node.swap_in_progress = True

        with patch.object(node.status_pub, 'publish') as mock_publish:
            node.publish_status()

            published_msg = mock_publish.call_args[0][0]
            assert "Swap: IN_PROGRESS" in published_msg.data

    def test_publish_status_swap_ready(self, node):
        """Test that publish_status shows READY when no swap in progress"""
        node.swap_in_progress = False

        with patch.object(node.status_pub, 'publish') as mock_publish:
            node.publish_status()

            published_msg = mock_publish.call_args[0][0]
            assert "Swap: READY" in published_msg.data


if __name__ == '__main__':
    pytest.main([__file__])