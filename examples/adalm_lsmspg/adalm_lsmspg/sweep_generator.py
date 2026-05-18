# Copyright 2026 Analog Devices, Inc.
#
# SPDX-License-Identifier: ADIBSD

"""
ROS2 Sweep Generator Node - ADALM-LSMSPG Demo

This node generates a sinusoidal sweep pattern for servo position commands.
It publishes position commands that sweep smoothly between min and max angles,
simulating a robotic arm doing repetitive motion.
"""

import math

import rclpy
from rclpy.node import Node, ParameterDescriptor
from std_msgs.msg import Float64


class SweepGenerator(Node):
    """Generates sinusoidal sweep pattern for servo position commands."""

    def __init__(self):
        super().__init__('sweep_generator')

        self.declare_parameter(
            'sweep_rate_hz',
            0.5,
            descriptor=ParameterDescriptor(
                description='Frequency of the sweep pattern in Hz.'
            )
        )
        self.declare_parameter(
            'min_angle',
            0.0,
            descriptor=ParameterDescriptor(
                description='Minimum angle in degrees.'
            )
        )
        self.declare_parameter(
            'max_angle',
            180.0,
            descriptor=ParameterDescriptor(
                description='Maximum angle in degrees.'
            )
        )
        self.declare_parameter(
            'update_rate_hz',
            10.0,
            descriptor=ParameterDescriptor(
                description='Rate at which to publish position commands.'
            )
        )
        self.declare_parameter(
            'position_topic',
            'servo/position_cmd',
            descriptor=ParameterDescriptor(
                description='Topic to publish position commands.'
            )
        )
        self.declare_parameter('qos', 10)

        self.sweep_rate = float(self.get_parameter('sweep_rate_hz').value)
        self.min_angle = float(self.get_parameter('min_angle').value)
        self.max_angle = float(self.get_parameter('max_angle').value)
        update_rate = float(self.get_parameter('update_rate_hz').value)
        position_topic = self.get_parameter('position_topic').value
        qos = int(self.get_parameter('qos').value)

        self.position_pub = self.create_publisher(Float64, position_topic, qos)

        self.time_elapsed = 0.0
        self.timer_period = 1.0 / update_rate
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

        self.get_logger().info(
            f'Sweep Generator started - sweeping {self.min_angle} to {self.max_angle} deg '
            f'at {self.sweep_rate} Hz'
        )

    def timer_callback(self):
        self.time_elapsed += self.timer_period

        mid = (self.min_angle + self.max_angle) / 2.0
        amplitude = (self.max_angle - self.min_angle) / 2.0
        angle = mid + amplitude * math.sin(2 * math.pi * self.sweep_rate * self.time_elapsed)

        msg = Float64()
        msg.data = angle
        self.position_pub.publish(msg)

        self.get_logger().debug(f'Position command: {angle:.1f} deg')


def main(args=None):
    rclpy.init(args=args)
    node = SweepGenerator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Sweep Generator stopped by user')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
