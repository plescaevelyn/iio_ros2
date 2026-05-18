# Copyright 2026 Analog Devices, Inc.
#
# SPDX-License-Identifier: ADIBSD

"""
Main bringup launch file for ADALM-LSMSPG servo demo.
Launches configuration and demo nodes.
"""

import os

from ament_index_python import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    pkg_dir = get_package_share_directory('adalm_lsmspg')
    launch_dir = os.path.join(pkg_dir, 'launch')

    config_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_dir, 'adalm_lsmspg_config.launch.py')
        ),
    )

    topics_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_dir, 'adalm_lsmspg_topics.launch.py')
        ),
    )

    servo_commander_node = Node(
        package='adalm_lsmspg',
        executable='servo_commander',
        name='servo_commander',
        output='screen',
        parameters=[{
            'loop_rate': 10.0,
            'dac_raw': 'ad5592r/output_voltage0/raw',
            'dac_scale': 'ad5592r/output_voltage0/scale',
            'position_topic': 'servo/position_cmd',
            'min_angle': 0.0,
            'max_angle': 180.0,
            'max_voltage_mv': 2500.0,
        }],
    )

    servo_feedback_node = Node(
        package='adalm_lsmspg',
        executable='servo_feedback',
        name='servo_feedback',
        output='screen',
        parameters=[{
            'timer_period': 0.1,
            'position_adc_raw': 'ad5592r/input_voltage1/raw',
            'position_adc_scale': 'ad5592r/input_voltage1/scale',
            'current_adc_raw': 'ad5592r/input_voltage2/raw',
            'current_adc_scale': 'ad5592r/input_voltage2/scale',
            'max_voltage_mv': 2500.0,
            'max_angle': 180.0,
            'current_sense_resistor': 47.0,
        }],
    )

    sweep_generator_node = Node(
        package='adalm_lsmspg',
        executable='sweep_generator',
        name='sweep_generator',
        output='screen',
        parameters=[{
            'sweep_rate_hz': 0.5,
            'min_angle': 0.0,
            'max_angle': 180.0,
            'update_rate_hz': 10.0,
            'position_topic': 'servo/position_cmd',
        }],
    )

    delayed_nodes = TimerAction(
        period=2.0,
        actions=[
            servo_commander_node,
            servo_feedback_node,
            sweep_generator_node,
        ],
    )

    return LaunchDescription([
        config_launch,
        topics_launch,
        delayed_nodes,
    ])
