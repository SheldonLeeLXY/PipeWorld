# pipeworld
Gazebo worlds with pipe networks

## Build
Requires ros-foxy and gazebo >= 11
in main folder, after having sourced you ros-foxy environment:
    colcon build
    source install/setup.bash 
    

## Launch
### Empty pipe world:
in main folder:

    ros2 launch pipeworld world.launch.py 
    
this command will load a preset pipe network. To set your own network, you can specify the bend points with the 'points' option and/or the diameter of the pipes with 'diameter'. E.g.:

    ros2 launch pipeworld world.launch.py points:='(-1,0) (3,2) (3.5,-4)' diameter:=0.3
    
do try and avoid acute angles as parts of the pipe will overlap.
    
### Pipe world with a sprintbot:
You will need the sprintbot-model package to launch this setup.

in main folder:

    ros2 launch pipeworld sprintbot_world.launch.py 
    
You can then control the sprintbot with another ros2 node or with another terminal.
The sprintbot topics are all in the /sprintbot/ namespace (this is set in the launch file).

For example, to make the sprintbot go forward, type:

    ros2 topic pub /sprintbot/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.5, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
    
into another terminal (with your ros2 environment sourced).

