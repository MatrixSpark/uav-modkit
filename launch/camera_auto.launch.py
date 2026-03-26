from launch import Launcher
from launch_ros.actions import Node


def camera_auto_launcher():

    # Camera detector identifies which camera hardware is present
    detector = Node(
        package='camera_sensor',
        executable='camera_detector',
        name='camera_detector',
        output='screen'
    )

    # libcamera-based camera node (publishes /camera/image_raw)
    libcamera = Node(
        package='camera_sensor',
        executable='libcamera_node',
        name='libcamera_node',
        output='screen',
        parameters=[{
            'vendor': 'libcamera',
            'enabled': False   # Enabled dynamically by deployment manager
        }]
    )

    # Simple payload adapter for camera data
    payload_adapter = Node(
        package='camera_sensor',
        executable='camera_payload_adapter',
        name='camera_payload_adapter',
        output='screen'
    )

    return Launcher([
        detector,
        libcamera,
        payload_adapter
    ])


def generate_launch_description():
    return camera_auto_launcher()
