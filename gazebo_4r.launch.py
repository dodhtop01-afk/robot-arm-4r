import os

from launch import LaunchDescription
from launch.actions import (
    IncludeLaunchDescription,
    RegisterEventHandler,
    SetEnvironmentVariable,
)
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import (
    PythonLaunchDescriptionSource,
)

from launch_ros.actions import Node

from ament_index_python.packages import (
    get_package_share_directory,
)


def generate_launch_description():

    project_dir = os.path.expanduser("~/robot_arm_4r")

    urdf_path = os.path.join(
        project_dir,
        "models",
        "arm_4r_control.urdf"
    )

    gazebo_launch_path = os.path.join(
        get_package_share_directory("gazebo_ros"),
        "launch",
        "gazebo.launch.py"
    )

    # Read robot description
    with open(urdf_path, "r") as file:
        robot_description = file.read()

    # Gazebo Classic Server
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            gazebo_launch_path
        ),
        launch_arguments={
            "gui": "false",
        }.items()
    )

    # Publish robot description and TF
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[
            {
                "robot_description": robot_description,
                "use_sim_time": True,
            }
        ]
    )

    # Spawn robot into Gazebo
    spawn_robot = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        name="spawn_robot_4r",
        output="screen",
        arguments=[
            "-entity", "robot_arm_4r",
            "-file", urdf_path,
            "-x", "0",
            "-y", "0",
            "-z", "0",
        ]
    )

    # Joint state broadcaster
    joint_state_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager",
        ],
        output="screen"
    )

    # Joint trajectory controller
    arm_controller = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "arm_controller",
            "--controller-manager",
            "/controller_manager",
        ],
        output="screen"
    )

    # Start broadcaster after robot spawn process exits
    start_broadcaster = RegisterEventHandler(
        OnProcessExit(
            target_action=spawn_robot,
            on_exit=[joint_state_broadcaster]
        )
    )

    # Start arm controller after broadcaster process exits
    start_arm_controller = RegisterEventHandler(
        OnProcessExit(
            target_action=joint_state_broadcaster,
            on_exit=[arm_controller]
        )
    )

    return LaunchDescription([
        SetEnvironmentVariable(
            "GAZEBO_MODEL_DATABASE_URI", ""
        ),
        gazebo,
        robot_state_publisher,
        spawn_robot,
        start_broadcaster,
        start_arm_controller,
    ])
