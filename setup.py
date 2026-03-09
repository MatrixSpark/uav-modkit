from setuptools import setup

package_name = 'lidar_sensor'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/lidar_auto.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    description='Unified ROS 2 LiDAR interface for multiple UAV payloads',
    license='Apache License 2.0',
    entry_points={
        'console_scripts': [
            'lidar_detector = lidar_sensor.detector_node:main',
            'riegl_lidar   = lidar_sensor.riegl_node:main',
            'vulcan_lidar  = lidar_sensor.vulcan_node:main',
            'harris_lidar  = lidar_sensor.harris_node:main',
            'lidar_payload_adapter = lidar_sensor.payload_manager_adapter:main',
        ],
    },
)
