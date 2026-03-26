from setuptools import setup

package_name = 'imu_sensor'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    description='Unified ROS 2 IMU interface for multiple UAV sensor modules',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'imu_detector = imu_sensor.imu_detector:main',
            'imu_payload_adapter = imu_sensor.payload_adapter:main',
            'bosch_bno055_imu = imu_sensor.bosch_bno055:main',
        ],
    },
)
