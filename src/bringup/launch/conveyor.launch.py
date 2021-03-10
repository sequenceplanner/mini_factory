import os

import launch
from launch.actions import GroupAction
import launch_ros.actions
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
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
            sp,
            sp_ui,
             ]
    return launch.LaunchDescription(nodes)
