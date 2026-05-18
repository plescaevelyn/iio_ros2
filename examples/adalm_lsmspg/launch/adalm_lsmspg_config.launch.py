# Copyright 2026 Analog Devices, Inc.
#
# SPDX-License-Identifier: ADIBSD

"""
Launch file to configure AD5592R channels for servo demo.
Sets up DAC output on channel 0 and ADC inputs on channels 1 and 2.
"""

from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch.substitutions import FindExecutable


def generate_launch_description():
    scale = 0.6103515629
    raw = 0

    ch0_dac_cfg = ExecuteProcess(
        cmd=[
            [FindExecutable(name='ros2'),
             ' service call ',
             ' /adi_iio_node/AttrWriteString adi_iio/srv/AttrWriteString ',
             f"\"{{ \
                attr_path: 'ad5592r/output_voltage0/scale', \
                value: {scale} \
            }}\" ;"],
            [FindExecutable(name='ros2'),
             ' service call ',
             ' /adi_iio_node/AttrWriteString adi_iio/srv/AttrWriteString ',
             f"\"{{ \
                attr_path: 'ad5592r/output_voltage0/raw', \
                value: {raw} \
            }}\" ;"],
        ],
        shell=True,
    )

    ch1_adc_cfg = ExecuteProcess(
        cmd=[
            [FindExecutable(name='ros2'),
             ' service call ',
             ' /adi_iio_node/AttrWriteString adi_iio/srv/AttrWriteString ',
             f"\"{{ \
                attr_path: 'ad5592r/input_voltage1/scale', \
                value: {scale} \
            }}\" ;"],
        ],
        shell=True,
    )

    ch2_adc_cfg = ExecuteProcess(
        cmd=[
            [FindExecutable(name='ros2'),
             ' service call ',
             ' /adi_iio_node/AttrWriteString adi_iio/srv/AttrWriteString ',
             f"\"{{ \
                attr_path: 'ad5592r/input_voltage2/scale', \
                value: {scale} \
            }}\" ;"],
        ],
        shell=True,
    )

    return LaunchDescription([
        ch0_dac_cfg,
        ch1_adc_cfg,
        ch2_adc_cfg,
    ])
