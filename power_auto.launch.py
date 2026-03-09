from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([

        # ---------------------------------------------------------
        # Range Sensor Detector
        # ---------------------------------------------------------
        Node(
            package='power_sensor',
            executable='range_detector',
            name='range_detector',
            output='screen'
        ),

        # ---------------------------------------------------------
        # Battery State Detector
        # ---------------------------------------------------------
        Node(
            package='power_sensor',
            executable='battery_state_detector',
            name='battery_state_detector',
            output='screen'
        ),

        # ---------------------------------------------------------
        # Battery Control Supervisor
        # ---------------------------------------------------------
        Node(
            package='sensor_health',
            executable='battery_control',
            name='battery_control',
            output='screen',
            parameters=[{
                'low_threshold': 0.25,
                'critical_threshold': 0.10
            }]
        ),

        # ---------------------------------------------------------
        # Optional: Health Monitor (aggregates IMU/LiDAR/Battery)
        # ---------------------------------------------------------
        Node(
            package='sensor_health',
            executable='sensor_health_monitor',
            name='sensor_health_monitor',
            output='screen'
        ),
    ])
