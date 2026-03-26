# Common imports shared across IMU modules

from collections import deque

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from sensor_msgs.msg import BatteryState
from std_msgs.msg import String


class uavBuffer:
    """Simple fixed-size FIFO buffer for sensor samples and status messages."""

    def __init__(self, maxlen=100):
        if maxlen <= 0:
            raise ValueError("maxlen must be greater than 0")
        self._items = deque(maxlen=maxlen)

    def append(self, item):
        self._items.append(item)

    def snapshot(self):
        return list(self._items)

    def clear(self):
        self._items.clear()

    def __len__(self):
        return len(self._items)

    @property
    def maxlen(self):
        return self._items.maxlen


class dataHandler:
    """Manage separate named buffers for multiple payload streams."""

    def __init__(self, default_maxlen=100):
        if default_maxlen <= 0:
            raise ValueError("default_maxlen must be greater than 0")
        self._default_maxlen = default_maxlen
        self._routes = {}

    def ensure_route(self, route_name, maxlen=None):
        if not route_name:
            raise ValueError("route_name is required")
        if route_name not in self._routes:
            self._routes[route_name] = uavBuffer(maxlen or self._default_maxlen)
        return self._routes[route_name]

    def append(self, route_name, item):
        self.ensure_route(route_name).append(item)

    def get_route(self, route_name):
        return self._routes.get(route_name)

    def snapshot(self, route_name):
        route = self.get_route(route_name)
        return [] if route is None else route.snapshot()

    def clear(self, route_name=None):
        if route_name is None:
            for route in self._routes.values():
                route.clear()
            return
        route = self.get_route(route_name)
        if route is not None:
            route.clear()

    def remove_route(self, route_name):
        self._routes.pop(route_name, None)

    def route_names(self):
        return list(self._routes.keys())

    def __contains__(self, route_name):
        return route_name in self._routes

    def __len__(self):
        return len(self._routes)

__all__ = [
    "rclpy",
    "Node",
    "Imu",
    "BatteryState",
    "String",
    "uavBuffer",
    "dataHandler",
]
