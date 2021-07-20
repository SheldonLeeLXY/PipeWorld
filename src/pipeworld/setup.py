from setuptools import setup

package_name = 'pipeworld'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/world.launch.py']),
        ('share/' + package_name + '/launch', ['launch/sprintbot_world.launch.py']),
        ('share/' + package_name + '/launch', ['launch/flat_pipe.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Nicolas Cambier',
    maintainer_email='n.p.cambier@leeds.ac.uk',
    description='Gazebo worlds with pipe networks',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'pipe_spawner = pipeworld.pipe_spawner:main',
            'navi_pose = pipeworld.exploring_slam:main'
        ],
    },
)
