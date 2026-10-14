# PHASE 01 — Kinematic Modeling & Simulation

## 1. Project Objective

Develop a 4-DOF robotic manipulator for
kinematic analysis and ROS 2 simulation.

## 2. Robot Configuration

J1: Base Rotation
J2: Shoulder
J3: Elbow
J4: Wrist Pitch

## 3. Initial Dimensions

L1 = 0.10 m
L2 = 0.15 m
L3 = 0.15 m
L4 = 0.06 m

## Development Log — Phase 01

### Task: URDF Modeling

**Objective:**
Create a basic 4-DOF robotic arm model using URDF.

### What I learned

1. Link:
   A rigid body of the robot.
   Example: upper_arm, forearm, wrist.

2. Joint:
   Connects two links and defines their relative motion.
   Example: joint2 connects base_rotation and upper_arm.

3. Joint Axis:
   Defines the rotation axis of a joint.
   - J1: (0, 0, 1) -> Base rotation.
   - J2: (0, -1, 0) -> Shoulder.
   - J3: (0, -1, 0) -> Elbow.
   - J4: (0, -1, 0) -> Wrist pitch.

4. Joint Origin:
   Defines the position and orientation of a joint
   relative to its parent link.

### Implementation

Created:
models/arm_4r.urdf

Robot structure:
base_link -> base_rotation -> upper_arm
-> forearm -> wrist -> tool_link

### Verification

Command:
check_urdf models/arm_4r.urdf

Result:
Successfully Parsed XML.

Conclusion:
URDF structure is valid.
Joint motion and FK accuracy have not been verified yet.

### Next Step

Visualize the robot in RViz2 and test J1-J4.

## 4. Learning Goals

- Understand robot joint configuration
- Derive Forward Kinematics
- Implement FK using Python
- Visualize robot in RViz2
- Validate mathematical results

## 5. Progress

- [x] Define robot geometry
- [x] Implement FK
- [x] Create URDF
- [x] Visualize in RViz2
- [x] Validate FK against ROS 2 TF
- [ ] Implement Inverse Kinematics
- [ ] Connect IK to ROS 2
- [ ] Generate robot trajectories
- [ ] Integrate MediaPipe

## 6. Questions and Observations

(To be updated during development)

## Forward Kinematics Implementation

### Objective
Calculate end-effector position from joint angles.

### Method
Analytical FK using trigonometric equations.

### Input
q1, q2, q3, q4 (radians)

### Output
End-effector position (x, y, z)

### Validation
Compare Python FK results with ROS 2 TF.

### Expected Zero Configuration
P = (0.36, 0.00, 0.10) meters

## FK Validation Results

### Test 1: Zero Configuration

Joint angles:
q1 = 0 rad
q2 = 0 rad
q3 = 0 rad
q4 = 0 rad

Python FK:
X = 0.360 m
Y = 0.000 m
Z = 0.100 m

ROS 2 TF:
Translation = [0.360, 0.000, 0.100]

### Conclusion

The analytical FK model is consistent with
the URDF-based ROS 2 transformation at the
tested zero configuration.

The displayed coordinate difference is zero
at three decimal places.

Further tests with nonzero joint angles are
needed for more comprehensive validation.


## Inverse Kinematics — ROS 2 Integration

### Objective
Compute joint angles from a target position
and visualize the result in RViz2.

### Implementation
- Implemented analytical IK for the 4R robot.
- Found two valid IK solutions.
- Verified both solutions using FK.
- Created a ROS 2 JointState publisher.
- Visualized an IK-generated robot configuration in RViz2.

### Test Target
Position: (0.20, 0.10, 0.15) m
Tool pitch: 0 degrees

### FK Verification
Both IK solutions produced the target position
with a displayed numerical error of 0.00000000 m.

### Current Limitations
- Target coordinates are hardcoded.
- Solution selection is manual.
- No trajectory generation.
- No physical actuator control.
- ROS 2 TF verification of the IK pose is pending.

### Next Step
Implement interactive target input and
automatic IK solution selection.

## Phase 01 — Step 09 Completed

### Feature
Automatic IK Solution Selection

### Implementation
- Added Auto mode to IK Controller.
- Implemented nearest-solution selection.
- Integrated automatic selection with
  cubic trajectory interpolation.

### Verification
3/3 functional tests passed.

### Result
The robot can automatically select an IK
configuration close to its current pose.

### Status
Completed for the current kinematic simulator.
