FROM osrf/ros:jazzy-desktop

SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-colcon-common-extensions \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /ws
COPY . /ws

RUN source /opt/ros/jazzy/setup.bash && \
    colcon build --symlink-install --base-paths camera imu lidar power

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash", "-lc", "ros2 pkg list | grep -E 'imu_sensor|camera_sensor|lidar_sensor|power_mgr' || true"]
