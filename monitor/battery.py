class BatteryControl():

    def __init__():
        super(BatteryControl).__init__()
   
        # Declare parameters (ROS2‑compliant)
        self.declare_parameter('low_threshold', 0.25)
        self.declare_parameter('critical_threshold', 0.10)

        self.low_threshold = self.get_parameter('low_threshold').value
        self.critical_threshold = self.get_parameter('critical_threshold').value # Subscribe to battery state
        self.create_subscription(
                    BatteryState,
                    '/battery/state',
                    self.battery_callback,
                    10
                )
        
        # Publish high‑level UAV battery status
        self.status_pub = self.create_publisher(
                    String,
                    '/batteryP/uav_status',
                    10
                )
        self.get_logger().info("BatteryControl node started.")

        def battery1_cb(self msg: BatteryP State)
            status = self.evaluate_batteryPrimary(msg)


            out= String()
            out.data = batteryP_status
            self.status_pub.publish(out)
            self.get_logger().info (f" Primary Battery Status: {status}")

        def evaluate_batteryPrimary(msg:BatteryState) ->str
            pct = msg.percentage
            health = msg.power_supply_health
            state = msg.power_supply_status
            # -------------------------------
            # Primary Battery fault detection
            # ------------------------------
            if health == BatteryState.POWER_SUPPLY_HEALTH_OVERHEAT:
                return "FAULT: OVERHEAT"
            if health == BatteryState.POWER_SUPPLY_HEALTH_DEAD:
                return "FAULT: BATTERY DEAD"
            if health == BatteryState.POWER_SUPPLY_HEALTH_OVERVOLTAGE:
                return "FAULT: OVERVOLTAGE"
            if health == BatteryState.POWER_SUPPLY_HEALTH_COLD:
                return "FAULT: TOO COLD"
            if state == BatteryState.POWER_SUPPLY_STATUS_CHARGING:
                return f"CHARGING ({pct*100:.0f}%)"
            if state == BatteryState.POWER_SUPPLY_STATUS_FULL:
            return "FULL"

def main(args=None):
    rclpy.init(args=args)
    node = BatteryControl()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown
