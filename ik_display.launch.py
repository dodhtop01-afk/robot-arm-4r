from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    urdf_path = (
        '/home/quanviem/robot_arm_4r/'
        'models/arm_4r.urdf'
    )

    with open(urdf_path, 'r') as file:
        robot_description = file.read()

    return LaunchDescription([

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': ParameterValue(
                    robot_description,
                    value_type=str
                )
            }]
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=[
                '-d',
                '/opt/ros/humble/share/'
                'urdf_tutorial/rviz/urdf.rviz'
            ]
        )

    ])
