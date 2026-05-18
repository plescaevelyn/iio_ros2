# Copyright 2026 Analog Devices, Inc.
#
# SPDX-License-Identifier: ADIBSD

"""
Launch file to enable IIO attribute topics for servo demo.
Enables DAC output topic and ADC input topics.
"""

from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch.substitutions import FindExecutable


def generate_launch_description():
    loop_rate = 10.0

    ch0_dac_topic = ExecuteProcess(
        cmd=[
            [FindExecutable(name='ros2'),
             ' service call ',
             ' /adi_iio_node/AttrEnableTopic adi_iio/srv/AttrEnableTopic ',
             f"\"{{ \
                attr_path: 'ad5592r/output_voltage0/raw', \
                loop_rate: {loop_rate} \
            }}\" ;"],
        ],
        shell=True,
    )

    ch1_adc_topic = ExecuteProcess(
        cmd=[
            [FindExecutable(name='ros2'),
             ' service call ',
             ' /adi_iio_node/AttrEnableTopic adi_iio/srv/AttrEnableTopic ',
             f"\"{{ \
                attr_path: 'ad5592r/input_voltage1/raw', \
                loop_rate: {loop_rate} \
            }}\" ;"],
        ],
        shell=True,
    )

    ch2_adc_topic = ExecuteProcess(
        cmd=[
            [FindExecutable(name='ros2'),
             ' service call ',
             ' /adi_iio_node/AttrEnableTopic adi_iio/srv/AttrEnableTopic ',
             f"\"{{ \
                attr_path: 'ad5592r/input_voltage2/raw', \
                loop_rate: {loop_rate} \
            }}\" ;"],
        ],
        shell=True,
    )

    return LaunchDescription([
        ch0_dac_topic,
        ch1_adc_topic,
        ch2_adc_topic,
    ])
