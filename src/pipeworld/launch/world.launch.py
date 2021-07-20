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
import sys


def generate_launch_description():
    gazebo_path = get_package_share_directory('gazebo_ros')
    world = get_package_share_directory('pipeworld')+'/worlds/pipe.world'

    pipe_arguments = []
    for arg in sys.argv:
        if(arg == 'pause:=true'):
            pipe_arguments.append('--pause')
        elif('points:=' in arg):
            pipe_arguments.append('--points')
            pipe_arguments.append(arg.replace('points:=',''))
        elif('diameter:=' in arg):
            pipe_arguments.append('-d')
            pipe_arguments.append(arg.replace('diameter:=',''))
    
    pipe_spawner = Node(
        package='pipeworld',
        executable='pipe_spawner',
        output='screen',
        arguments=pipe_arguments
    )
    
    return LaunchDescription([
        DeclareLaunchArgument(
            'world', default_value=world,
            description='Specify world file name'
        ),
        DeclareLaunchArgument(
            'pause', default_value='true',
            description='Set "true" to start the server in a paused state.'
        ),
        
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([gazebo_path, '/launch/gazebo.launch.py'])
        ),

        pipe_spawner
        
    ])
