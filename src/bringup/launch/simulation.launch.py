import os

import launch
from launch.actions import GroupAction
import launch_ros.actions
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    control_box = launch_ros.actions.Node(
        package='control_box_driver',
        executable='control_box_dummy',
        namespace='/control_box',
        output='screen',
    )

    sp = launch_ros.actions.Node(
                package='sp_model',
                executable='mini',
                output={'both': 'log'}, # output='screen',
                arguments = ['--ros-args', '--log-level', 'INFO'],
                )

    sp_ui = launch_ros.actions.Node(
                package='sp_ui',
                executable='sp_ui',
                namespace='/',
                output='screen',
                )

    nodes = [
        control_box,
        sp,
        # sp_ui,
    ]

    return launch.LaunchDescription(nodes)
