from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
from launch import LaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription 
import os

def generate_launch_description():
    gazebo_sim_path = os.path.join(get_package_share_directory(
                        'turtlebot3_gazebo'),
                        'launch',
                        'empty_world.launch.py') 
    gesture_recognition = Node(
        package = 'turtlebot3_nodes',
        executable = 'turtlebot3_gesture_publisher',
        name = 'turtlebot3_gesture_publisher',
        output = 'screen'
    )
    cmd_vel = Node(
        package = 'turtlebot3_nodes',
        executable= 'turtlebot3_cmd_vel',
        name = 'turtlebot3_cmd_vel',
        output = 'screen'
    )
    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(gazebo_sim_path)
        ),
        gesture_recognition,
        cmd_vel
    ])