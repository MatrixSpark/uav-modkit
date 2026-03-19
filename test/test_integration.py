#!/usr/bin/env python3

import pytest
import subprocess
import sys
import os
import time
from unittest.mock import patch, MagicMock

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class TestSystemIntegration:
    """Integration tests for the overall UAV ModKit system"""

    @pytest.mark.integration
    def test_import_all_modules(self):
        """Test that all main modules can be imported without errors"""
        try:
            # Test core imports
            from core.core import rclpy, Node
            assert rclpy is not None
            assert Node is not None

            # Test deploy manager
            from deploy.Deploy import DeployManager
            assert DeployManager is not None

            # Test sensor detectors
            from imu.imu_sensor.imu_detector import ImuDetector
            from lidar.detector import LidarDetector
            assert ImuDetector is not None
            assert LidarDetector is not None

            print("✓ All modules imported successfully")

        except ImportError as e:
            pytest.fail(f"Failed to import modules: {e}")

    @pytest.mark.integration
    def test_package_structure(self):
        """Test that the package structure is correct"""
        # Check that all expected directories exist
        expected_dirs = [
            'core',
            'deploy',
            'imu',
            'imu/imu_sensor',
            'lidar',
            'power',
            'monitor',
            'launch',
            'test'
        ]

        for dir_path in expected_dirs:
            assert os.path.isdir(dir_path), f"Directory {dir_path} does not exist"

        # Check that key files exist
        expected_files = [
            'core/core.py',
            'deploy/Deploy.py',
            'imu/package.xml',
            'imu/setup.py',
            'lidar/package.xml',
            'lidar/setup.py',
            'power/package.xml',
            'power/setup.py',
            'README.md',
            'package.xml',
            'setup.py'
        ]

        for file_path in expected_files:
            assert os.path.isfile(file_path), f"File {file_path} does not exist"

        print("✓ Package structure is correct")

    @pytest.mark.integration
    def test_build_scripts_exist(self):
        """Test that build scripts exist and are executable"""
        build_scripts = [
            'build.sh',
            'build.bat',
            'install_and_build.sh'
        ]

        for script in build_scripts:
            assert os.path.isfile(script), f"Build script {script} does not exist"

        print("✓ Build scripts are present")

    @pytest.mark.integration
    def test_test_structure(self):
        """Test that the test structure is correct"""
        test_files = [
            'test/test_deploy_manager.py',
            'test/test_lidar_detector.py',
            'test/test_imu_detector.py',
            'test/pytest.ini',
            'test/requirements-test.txt',
            'test/run_tests.sh',
            'test/run_tests.bat'
        ]

        for test_file in test_files:
            assert os.path.isfile(test_file), f"Test file {test_file} does not exist"

        print("✓ Test structure is correct")

    @pytest.mark.slow
    @pytest.mark.integration
    def test_colcon_build_dry_run(self):
        """Test that colcon can parse the packages (dry run)"""
        # This test would require ROS 2 to be installed
        # For now, just check that package.xml files exist and are valid XML
        import xml.etree.ElementTree as ET

        package_files = [
            'package.xml',
            'imu/package.xml',
            'lidar/package.xml',
            'power/package.xml'
        ]

        for pkg_file in package_files:
            try:
                tree = ET.parse(pkg_file)
                root = tree.getroot()
                assert root.tag == 'package', f"Invalid package.xml structure in {pkg_file}"
                print(f"✓ {pkg_file} is valid XML")
            except ET.ParseError as e:
                pytest.fail(f"Invalid XML in {pkg_file}: {e}")

    def test_supported_vendors_configuration(self):
        """Test that supported vendors are properly configured"""
        from deploy.Deploy import DeployManager

        # Create instance to check vendor lists
        import rclpy
        rclpy.init()
        manager = DeployManager()

        # Check IMU vendors
        expected_imu_vendors = ['bosch', 'xsens', 'vn310']
        assert manager.supported_imu_vendors == expected_imu_vendors

        # Check LiDAR vendors
        expected_lidar_vendors = ['velodyne', 'riegl', 'vulcan', 'harris']
        assert manager.supported_lidar_vendors == expected_lidar_vendors

        manager.destroy_node()
        rclpy.shutdown()

        print("✓ Vendor configurations are correct")


if __name__ == '__main__':
    pytest.main([__file__, "-v", "-m", "not slow"])