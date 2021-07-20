# MIT License
#
# Copyright (c) 2021 University of Leeds
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.substitutions import ThisLaunchFileDir
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node


def generate_launch_description():
    gazebo_path = get_package_share_directory('gazebo_ros')
    pipeworld_path = get_package_share_directory('pipeworld')
    world_description = pipeworld_path+'/worlds/pipe.world'
    urdf = get_package_share_directory('sprintbot-model')+'/urdf/sprintbot.urdf'

    params = {'robot_description': open(urdf).read()}
    robot_spawner = Node(package='gazebo_ros', executable='spawn_entity.py', arguments=['-topic', 'robot_description', '-entity', LaunchConfiguration('rb_id'), '-robot_namespace', LaunchConfiguration('rb_id'), '-z','0.11'], output='screen')
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )
    return LaunchDescription([
        DeclareLaunchArgument(
            'world', default_value=world_description,
            description='Specify world file name'
        ),
        DeclareLaunchArgument(
            'rb_id', default_value='sprintbot',
            description='Specify robot identifier'
        ),
        
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([pipeworld_path, '/launch/world.launch.py'])
        ),
        robot_state_publisher,
        robot_spawner
        
    ])
