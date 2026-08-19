from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory

import os


def generate_launch_description():

    pkg_share = get_package_share_directory(
        'delivery_robot_description'
    )

    xacro_file = os.path.join(
        pkg_share,
        'urdf',
        'delivery_robot.urdf.xacro'
    )

    world_file = os.path.join(
        pkg_share,
        'worlds',
        'delivery_world.sdf'
    )

    robot_description = Command([
        'xacro ',
        xacro_file
    ])

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            )
        ),
        launch_arguments={
            'gz_args': '-r -v 4 ' + world_file
        }.items()
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description
        }],
        output='screen'
    )

    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic',
            'robot_description',
            '-name',
            'delivery_robot',
            '-x',
            '0',
            '-y',
            '0',
            '-z',
            '0.15'
        ],
        output='screen'
    )

    return LaunchDescription([
        gazebo_launch,
        robot_state_publisher,
        spawn_robot
    ])