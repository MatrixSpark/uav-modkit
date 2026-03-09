import rclpy
from rclpy import Node
from std_msgs.msg import String

class SensorMonitor(Node):
    def __init__():
        super(SensorMonitor).__init__('Sensor_Health')

        #Monitor internal State
        self.imu_status = ""
        self.lidar_status = ""
        self.gps_status = ""
        self.batteryP_status = " "
        self.batteryS_status = " "
        self.frontcamera_status = " "
        self.barometer_status = " "

        #Subscriptions
        self.create_subscription(String,'/imu/status/',imu_cb, 10 )
        self.create_subscription(String,'/lidar/status/',lidar_cb, 10 )
        self.create_subscription(String,'/gps/status/',gps_cb, 10 )
        self.create_subscription(String,'/batteryP/status/',battery1_cb, 10 )
        self.create_subscription(String,'/frontcamera/status/',frontcamera_cb, 10 )
        self.create_subscription(String,'/barometer/status/',baro_cb, 10 )
        
        
        #Show UAV health
        self.health_pub = self.create_publisher(String, '/sensors/health', 10)


        # Timer
        self.timer = self.create_timer(1.0, self.sen_health)

    
    def imu_cb():
        self.imu_status = msg.data
    def lidar_cb():
        self.lidar_status= msg.data
    
    def gps_cb():
        self.gps_status =msg.data

    def battery1_cb():
        self.batteryP_status = msg.data
    def frontcamera_cb():
        self.frontcamera_status = msg.data
    
    def baro_cb():
        self.barometer_status = msg.data

    def sen_health():
        self.Sensor_Health = msg.data

        
