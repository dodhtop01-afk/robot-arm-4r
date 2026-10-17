# PHASE 03 — Step 05: Workspace Mapping and IK Validation

## Objective

Convert normalized 2D hand displacement into candidate
Cartesian targets for the 4R robot.

Validate target reachability using the existing analytical
inverse kinematics and forward kinematics.

## Architecture

Hand Motion
    |
    v
Workspace Mapping
    |
    v
Cartesian Target (X, Y, Z, Pitch)
    |
    v
Inverse Kinematics
    |
    v
Forward Kinematics Verification

## Mapping

Reference target:

X0 = 0.20 m
Y0 = 0.10 m
Z0 = 0.15 m

Mapping equations:

X = 0.20
Y = 0.10 + 0.08 * DX
Z = 0.15 + 0.08 * DY
Pitch = 0 rad

Configured limits:

Y: [0.06, 0.14] m
Z: [0.11, 0.19] m

These values are experimental.

## Implementation

- vision/workspace_mapping.py
- vision/ik_validation.py
- vision/workspace_ik_demo.py

Existing algorithms reused:

- scripts/inverse_kinematics.py
- scripts/forward_kinematics.py

## Observed Results

| Target XYZ (m) | IK Result |
|---|---|
| (0.200, 0.086, 0.170) | REACHABLE |
| (0.200, 0.067, 0.147) | UNREACHABLE |
| (0.200, 0.087, 0.147) | REACHABLE |

These are examples from manual webcam tests.

The result depends on robot geometry, joint limits
and desired tool pitch.

## Limitations

- Only image-plane 2D motion is mapped.
- X is fixed.
- Hand-to-robot mapping is not camera-calibrated.
- Cartesian bounds do not guarantee IK reachability.
- The current demo uses the first valid IK solution.
- No continuous trajectory feasibility check.
- No collision checking.
- No ROS 2 commands are published.

## Next Step

Connect validated targets to a motion controller.

Requirements before commanding motion:

- Select IK solutions near the current joint state.
- Limit commanded motion rate and joint velocity.
- Define control enable/disable behavior.
- Handle tracking loss and unreachable targets.
- Prevent stale trajectories from continuing unchecked.

## Long-Term Demo Goal

Use hand motion and gestures to control a 4R arm
with a gripper to grasp, lift and release an object
spawned in Gazebo.

Optional extension:

Track a real-world object using camera vision,
estimate its pose and place a virtual representation
in the Gazebo environment.
