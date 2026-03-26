from launch import Launcher
from launch_ros.actions import Node

def lidar_auto_launcher():

    # Detector node identifies which LiDAR is physically present
    detector = Node(
        package='lidar_sensor',
        executable='lidar_detector',
        name='lidar_detector',
        output='screen'
    )

    # Velodyne driver
    velodyne = Node(
        package='lidar_sensor',
        executable='velodyne_driver',
        name='velodyne_lidar_node',
        output='screen',
        parameters=[{
            'vendor': 'velodyne',
            'enabled': False   # enabled dynamically by detector or payload manager
        }]
    )

    # Payload manager adapter (bridges LiDAR → UAV payload system)
    payload_adapter = Node(
        package='lidar_sensor',
        executable='lidar_payload_mgr',
        name='lidar_payload_adapter',
        output='screen'
    )

    return Launcher([
        detector,
        velodyne,
        payload_adapter
    ])


def generate_launch_description():
    return lidar_auto_launcher()
