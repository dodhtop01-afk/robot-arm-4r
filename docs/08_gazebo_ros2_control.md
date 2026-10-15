# PHASE 02 — Gazebo Simulation & ROS 2 Control

## 1. Objective

Develop a physics-enabled simulation environment for a custom
4-DOF robotic manipulator using Gazebo Classic and ROS 2 Humble.

Integrate the existing analytical inverse kinematics algorithm with
ROS 2 Control to execute joint-space trajectories in simulation.

### Expected capabilities

- Simulate the 4R manipulator in Gazebo.
- Provide collision geometry and inertial properties.
- Control all four revolute joints.
- Execute smooth joint-space trajectories.
- Read actual joint states from the simulation.
- Control the robot using a Cartesian IK GUI.

## 2. System Architecture

```text
User
  |
  v
Gazebo IK Control GUI
  |
  | Target: X, Y, Z, Pitch
  v
Analytical Inverse Kinematics
  |
  | q1, q2, q3, q4
  v
Trajectory Generation
  |
  | JointTrajectory
  v
/arm_controller/joint_trajectory
  |
  v
Joint Trajectory Controller
  |
  v
gazebo_ros2_control
  |
  v
Gazebo Classic — 4R Robot
  |
  | JointState feedback
  v
/joint_states
  |
  v
GUI — Actual Joint Angles
```

The GUI sends joint trajectories to the controller rather than
publishing joint states directly.

This separates motion commands from joint-state feedback.

## 3. Robot Configuration

The manipulator has four revolute joints.

| Joint | Function | Rotation axis |
|---|---|---|
| J1 | Base rotation | Z |
| J2 | Shoulder pitch | -Y |
| J3 | Elbow pitch | -Y |
| J4 | Wrist pitch | -Y |

### Geometric parameters

| Parameter | Value |
|---|---|
| L1 | 0.10 m |
| L2 | 0.15 m |
| L3 | 0.15 m |
| L4 | 0.06 m |

### Robot structure

```text
world
  |
  v
base_link
  |
  | joint1
  v
base_rotation
  |
  | joint2
  v
upper_arm
  |
  | joint3
  v
forearm
  |
  | joint4
  v
wrist
  |
  | tool_fixed
  v
tool_link
```

The world-to-base connection is fixed.

## 4. Physical Modeling

File:

`models/arm_4r_physics.urdf`

Physical properties were added to the robot model:

- Mass
- Inertial properties
- Collision geometry
- Visual geometry

Approximate link masses:

| Link | Mass |
|---|---:|
| base_link | 0.20 kg |
| base_rotation | 0.15 kg |
| upper_arm | 0.10 kg |
| forearm | 0.08 kg |
| wrist | 0.05 kg |

These values are preliminary simulation assumptions.

They are not measurements from a manufactured robot.

### URDF verification

The model was checked using:

```bash
check_urdf models/arm_4r_physics.urdf
gz sdf -p models/arm_4r_physics.urdf
```

Important lesson:

A URDF may pass a structural parser while still containing
incorrectly nested visual, collision or inertial elements.

SDF conversion was useful for identifying such problems.

## 5. Gazebo Classic Integration

Simulation environment:

- Ubuntu
- ROS 2 Humble
- Gazebo Classic 11

The robot is spawned into Gazebo using `gazebo_ros`.

Control-enabled model:

`models/arm_4r_control.urdf`

A `gazebo_ros2_control` plugin connects the simulated joints
to ROS 2 Control.

## 6. ROS 2 Control Architecture

Controller configuration:

`config/controllers.yaml`

### Controllers

1. `joint_state_broadcaster`
2. `arm_controller`

`arm_controller` uses:

`joint_trajectory_controller/JointTrajectoryController`

Command interface:

`position`

State interfaces:

`position`, `velocity`

Controlled joints:

`joint1`, `joint2`, `joint3`, `joint4`

The controller manager update rate is configured to 100 Hz.

### ROS topics

Trajectory command:

```text
/arm_controller/joint_trajectory
```

Joint feedback:

```text
/joint_states
```

The GUI uses the joint names to associate feedback values
with the correct joints.

Joint ordering in a JointState message must not be assumed
to match the ordering in the controller configuration.

## 7. Trajectory Generation

A cubic smoothstep profile is used:

```text
s(u) = 3u^2 - 2u^3
```

where:

```text
u = t / T
```

The desired joint position is:

```text
q(t) = q_start + s(u) * (q_goal - q_start)
```

Trajectory points are generated and sent using:

`trajectory_msgs/msg/JointTrajectory`

The GUI chooses a motion duration that accounts for
configured velocity and acceleration limits.

The trajectory controller receives the full trajectory
instead of a sequence of direct joint-state commands.

## 8. IK GUI Integration

File:

`scripts/gazebo_ik_control_gui.py`

Features:

- Cartesian X, Y, Z input
- Desired pitch input
- Analytical inverse kinematics
- IK configuration selection
- Automatic solution selection based on joint feedback
- Smooth joint-space trajectory generation
- Home-position command
- Actual joint-angle display
- Joint-state subscription

The GUI uses FK verification to check the chosen IK result
before publishing a trajectory.

### Important distinction

The GUI status indicating that a trajectory was sent is
not equivalent to confirmation that a ROS 2 action goal
completed successfully.

The current implementation publishes to a trajectory topic.

## 9. Verification Results

### Gazebo integration

The 4R model was successfully spawned in Gazebo.

All four joint interfaces were loaded by
`gazebo_ros2_control`.

### Controller activation

Both controllers were observed in the active state:

```text
joint_state_broadcaster  active
arm_controller           active
```

### Joint trajectory execution

A test trajectory was sent to:

`/arm_controller/joint_trajectory`

Joint positions were observed close to their target values,
with position errors below approximately 6.5e-5 rad
in that test.

### Cartesian IK test

Test target:

```text
X = 0.20 m
Y = 0.10 m
Z = 0.15 m
Pitch = 0 rad
```

Approximate joint feedback displayed by the GUI:

```text
J1 =  26.59 deg
J2 = -38.21 deg
J3 = 110.45 deg
J4 = -72.28 deg
```

FK calculated from these rounded angles produced:

```text
X = 0.199965 m
Y = 0.100092 m
Z = 0.150028 m
```

Position error:

```text
Approximately 0.000102 m = 0.102 mm
```

This verifies consistency between the kinematic model
and the joint angles reported by the GUI.

It is not an independent measurement of the Gazebo
end-effector world pose.

### Automatic launch

The launch file:

`gazebo_4r.launch.py`

successfully started Gazebo, the robot state publisher,
robot spawning and both controllers in one test.

A later session experienced loss of ROS 2 node discovery
and joint-state feedback, so long-running stability
has not yet been established.

## 10. Problems and Solutions

### Incorrect URDF nesting

Some collision and inertial elements were incorrectly
placed inside visual elements.

Solution:

Move collision and inertial elements directly under
their corresponding link elements.

### XML declaration parsing issue

An XML encoding declaration caused an error while
loading the robot model through the spawn utility.

Solution used:

Remove the problematic encoding declaration from the
generated URDF file.

### Controller manager initialization

The Gazebo ROS 2 Control plugin required
`robot_state_publisher` to provide the robot description.

Solution:

Start `robot_state_publisher` before or alongside
robot spawning.

### Gazebo graphical performance

Starting the Gazebo server and graphical client
separately worked better on the development machine.

The GPU-accelerated client ran at approximately 60 FPS
during successful tests.

## 11. Known Limitations

- Link inertial parameters are preliminary estimates.
- No real servo hardware has been integrated.
- No collision-avoidance algorithm is implemented.
- No independent end-effector world-pose verification
  has been recorded.
- GUI trajectory publishing does not provide action-result
  acknowledgement.
- Some joint velocity feedback was inconsistent with
  apparently stationary joint positions in an earlier test.
- A later Gazebo session lost ROS 2 node discovery and
  joint-state feedback.
- Repeated Gazebo multicast network errors were observed.
  A direct causal link to ROS 2 discovery failure has
  not been confirmed.
- The control URDF currently references the controller
  configuration using a machine-specific absolute path.
- The launch workflow still requires a separate
  `gzclient` process for the graphical interface.

## 12. How to Run

First check for leftover Gazebo processes:

```bash
pgrep -af 'gzserver|gzclient'
```

If an older simulation session is still running,
stop it before launching a new one.

### Terminal 1 — Launch ROS 2 and Gazebo server

```bash
cd ~/robot_arm_4r
source /opt/ros/humble/setup.bash
ros2 launch ./gazebo_4r.launch.py
```

### Terminal 2 — Start Gazebo GUI

```bash
gzclient
```

### Terminal 3 — Verify controller and feedback

```bash
source /opt/ros/humble/setup.bash
ros2 control list_controllers
ros2 topic info /joint_states
```

Expected controllers:

```text
joint_state_broadcaster  active
arm_controller           active
```

The `/joint_states` topic must have a publisher
before the GUI can receive joint feedback.

### Terminal 4 — IK GUI

```bash
cd ~/robot_arm_4r
source /opt/ros/humble/setup.bash
python3 scripts/gazebo_ik_control_gui.py
```

Do not start a second Gazebo server while another
server from this project is still running.

## 13. What I Learned

- URDF geometry and physical simulation properties
  are separate concerns.
- A valid URDF parser result does not guarantee
  successful Gazebo conversion.
- ROS 2 Control separates command interfaces from
  joint-state feedback.
- A controller being active does not necessarily prove
  that its expected topic is currently publishing.
- JointState data should be matched by joint name.
- Gazebo server, graphical client, robot description,
  controller manager and IK GUI form distinct components.
- Kinematic verification should not be confused with
  validation of physical dynamics.
- Reliable startup, logging and reproducibility are
  important parts of robotics software development.

## 14. Phase 02 Status

**Functional MVP achieved.**

The Gazebo simulation, ROS 2 Control integration
and Cartesian IK GUI have been demonstrated.

Long-running reliability and portability remain
open engineering tasks.

Next phase:

**PHASE 03 — Vision-Based Robot Control with MediaPipe**
