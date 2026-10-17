# PHASE 03 — Step 04: Hand Motion Tracking

## Objective

Track relative hand movement using MediaPipe landmarks.

The objective is to obtain normalized horizontal and
vertical displacement before mapping hand movement
into the robot workspace.

## Method

The hand reference point is calculated using:

P_hand = (P0 + P9) / 2

Where:

- P0: Wrist landmark
- P9: Middle finger MCP landmark

Displacement:

DX = X_filtered - X_reference
DY = Y_reference - Y_filtered

Positive DY indicates upward movement in the mirrored
camera image.

## Filtering

An Exponential Moving Average (EMA) is applied:

P_filtered = alpha * P_current
           + (1 - alpha) * P_previous

Parameters:

- Alpha = 0.25
- Deadzone = 0.015

These are experimental parameters.

## Implementation

Files:

- vision/hand_motion.py
- vision/hand_motion_demo.py

## Verification

Observed examples:

| Test | DX | DY |
|---|---:|---:|
| Hand raised | +0.043 | +0.110 |
| Hand lowered | +0.047 | -0.116 |
| Hand moved left | -0.468 | +0.051 |
| Reference reset | 0.000 | 0.000 |

Results indicate that the sign conventions and
reference reset work in the tested examples.

## Limitations

- Only 2D image-plane displacement is measured.
- Camera depth is not estimated.
- Landmark noise is not fully eliminated.
- EMA introduces response delay.
- Hand rotation can affect the reference point.
- Tracking loss resets the reference position.
- No robot workspace mapping has been implemented.
- No robot movement commands are generated.

## Next Step

PHASE 03 — Step 05: Workspace Mapping

Convert normalized hand displacement into candidate
robot target coordinates.

Validate workspace limits and inverse kinematics
before connecting the vision system to ROS 2.
