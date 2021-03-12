import os

import launch
from launch.actions import GroupAction
import launch_ros.actions
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    control_box = launch_ros.actions.Node(
        package='control_box_driver',
        executable='control_box_driver',
        namespace='/control_box',
        output='screen',
    )

    nodes = [ control_box ]

    return launch.LaunchDescription(nodes)
