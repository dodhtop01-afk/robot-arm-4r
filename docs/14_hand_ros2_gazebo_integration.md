# PHASE 03 — Step 06: Hand-Controlled Gazebo Simulation

## Objective

Connect MediaPipe hand tracking to the existing
4R robotic arm simulation through ROS 2 Control.

## Architecture

Webcam
  |
  v
MediaPipe Hand Tracking
  |
  v
2D Hand Motion Tracking
  |
  v
Workspace Mapping
  |
  v
IK Validation
  |
  v
UDP localhost
  |
  v
ROS 2 Bridge
  |
  v
Joint Trajectory Controller
  |
  v
Gazebo 4R Robot

## Implementation

Vision sender:

vision/hand_target_sender.py

ROS 2 bridge:

scripts/hand_ros2_bridge.py

## Operating Modes

DRY RUN:
- Receives target coordinates.
- Validates inverse kinematics.
- Selects a nearby IK solution.
- Does not publish joint trajectories.

LIVE:
- Receives target coordinates.
- Uses joint-state feedback.
- Selects a nearby IK solution.
- Limits commanded joint increments.
- Publishes joint trajectories to Gazebo.

## Configuration

Control interval: 0.1 s
Trajectory duration: 0.3 s
Maximum commanded joint increment:
0.5 rad/s * 0.1 s = 0.05 rad

These parameters are experimental and do not
guarantee acceleration or continuous velocity limits.

## Verification

DRY RUN:
PASS — Target coordinates and joint angles
were calculated and displayed.

Timeout detection:
PASS — The bridge detected missing target updates.

LIVE:
PASS — The Gazebo robot responded to hand movement.

Observed behavior:

- Raising and lowering the hand produced
  corresponding robot posture changes.
- Horizontal hand movement changed the
  robot base rotation.
- Movement was not consistently smooth.
- Occasional sudden joint movements were observed.

Gazebo operated at approximately 60 FPS
during the demonstrated sessions.

## Important Limitations

- Frequent trajectory replacement may cause jitter.
- No measured tracking error has been recorded.
- No independent end-effector trajectory validation.
- No acceleration-aware trajectory planner.
- No collision avoidance.
- No gripper.
- UDP communication is intended for local simulation.
- The bridge does not yet provide robust
  trajectory cancellation or emergency stopping.
- Missing joint feedback prevents new commands,
  but does not guarantee an active trajectory stops.

## Next Step

Step 06.4 — Motion Smoothing and Controller Stability

Investigate:
- Trajectory replacement frequency.
- Joint-state tracking error.
- Motion velocity and acceleration limits.
- Feedback freshness.
- Safe handling of tracking loss.

Long-term goal:

Hand-controlled grasping, lifting and releasing
of a simulated object using a 4R arm and gripper.
