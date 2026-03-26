@echo off
setlocal

docker run --rm -it uav-modkit:jazzy bash -lc "ros2 launch /ws/launch/imu_auto.launch.py"

endlocal
