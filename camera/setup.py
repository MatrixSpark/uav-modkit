from setuptools import setup

package_name = 'camera_sensor'

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
    description='ROS 2 camera sensor support using libcamera/USB video devices.',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'camera_detector = camera_sensor.camera_detector:main',
            'libcamera_node = camera_sensor.libcamera_node:main',
            'camera_payload_adapter = camera_sensor.payload_adapter:main',
        ],
    },
)
