from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

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
        executable='velodyne_lidar',
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
        executable='lidar_payload_adapter',
        name='lidar_payload_adapter',
        output='screen'
    )

    return LaunchDescription([
        detector,
        velodyne,
        payload_adapter
    ])
