from setuptools import setup, find_packages
import os
from glob import glob

package_name = 'lidar_sensor'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='UAV Development Team',
    author_email='dev@example.com',
    description='Unified ROS 2 LiDAR interface for multiple UAV payloads',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'lidar_detector = lidar_sensor.detector:main',
            'lidar_payload_mgr = lidar_sensor.payload_mgr:main',
            'velodyne_driver = lidar_sensor.velodyne:main',
        ],
    },
)
