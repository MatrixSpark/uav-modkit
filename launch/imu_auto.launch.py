from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    # Detector node identifies the IMU which is physically present
    detector = Node(
        package='imu',
        executable='imu_detector',
        name='imu_detector',
        output='screen'
    )

    # Bosch BNO055 IMU driver
    bosch_bno055 = Node(
        package='imu',
        executable='bosch_bno055_imu',
        name='bosch_bno055_imu_node',
        output='screen',
        parameters=[{
            'vendor': 'bosch_bno055',
            'enabled': False   # default by payload manager
        }]
    )

    # Payload adaptor
    payload_adapter = Node(
        package='imu',
        executable='imu_payload_adapter',
        name='imu_payload_adapter',
        output='screen'
    )

    return LaunchDescription([
        detector,
        bosch_bno055,
        payload_adapter
    ])
