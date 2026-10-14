# 4-DOF Robot Arm — ROS 2

A 4-DOF robotic arm project developed using Python, ROS 2 Humble, URDF, and RViz2.

## Overview

This project explores robotic arm kinematics, inverse kinematics, and joint-space trajectory generation.

**Current status:** Phase 01 completed — kinematic simulation.

## Features

- Custom 4-DOF robot URDF
- Forward kinematics (FK)
- Analytical inverse kinematics (IK)
- ROS 2 / RViz2 visualization
- Interactive IK control GUI
- Automatic IK solution selection
- Cubic smoothstep trajectory generation
- Joint velocity and acceleration constraints

## Project Structure

```text
robot_arm_4r/
├── docs/                    # Technical documentation
├── models/                  # Robot URDF
├── scripts/                 # FK, IK, GUI and ROS 2 scripts
├── ik_display.launch.py     # RViz2 launch file
└── README.md
```

## Requirements

- Ubuntu 22.04
- ROS 2 Humble
- Python 3
- RViz2
- Tkinter

## Run the Simulation

Terminal 1:

```bash
cd ~/robot_arm_4r
source /opt/ros/humble/setup.bash
ros2 launch ./ik_display.launch.py
```

Terminal 2:

```bash
cd ~/robot_arm_4r
source /opt/ros/humble/setup.bash
python3 scripts/ik_control_gui.py
```

## Development Roadmap

- [x] Phase 01 — Kinematic modeling and RViz2 simulation
- [ ] Phase 02 — Gazebo dynamic simulation
- [ ] Phase 03 — MediaPipe-based robot control
- [ ] Phase 04 — Experimental validation and documentation

## Current Limitations

This project currently provides kinematic simulation only.

Collision avoidance, actuator feedback, and physical hardware control are not yet implemented.
