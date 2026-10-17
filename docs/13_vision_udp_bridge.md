# PHASE 03 — Step 06.2: Vision-to-ROS Bridge

## Objective

Establish communication between the MediaPipe
virtual environment and the ROS 2 Python environment.

## Architecture

MediaPipe
    |
    v
Hand Motion Tracking
    |
    v
Workspace Mapping
    |
    v
IK Validation
    |
    v
UDP localhost:5005
    |
    v
Python Receiver

## Implementation

Files:

- vision/hand_target_sender.py
- scripts/hand_target_receiver_test.py

## Communication

Protocol: UDP
Address: 127.0.0.1
Port: 5005

Maximum sending frequency: 10 Hz.

Packet fields:

- seq
- x
- y
- z
- pitch

Only IK-reachable targets are transmitted.

## Verification

- MediaPipe detected hand landmarks.
- Workspace mapping produced XYZ targets.
- IK validation identified reachable targets.
- Receiver successfully received UDP packets.
- Sequence numbers increased.
- Target coordinates changed with hand movement.
- Receiver detected the absence of recent packets.

Result: PASS.

## Limitations

- UDP delivery is not guaranteed.
- No authentication or packet integrity mechanism.
- No explicit tracking-status message.
- No ROS 2 trajectory commands are generated.
- No motion safety checks have been integrated.
- Timeout currently indicates absence of packets,
  not necessarily loss of hand tracking.

## Next Step

Step 06.3: ROS 2 Joint Trajectory Bridge.

Requirements:

- Read actual joint states.
- Select the nearest valid IK solution.
- Limit joint velocity and target update frequency.
- Reject stale or invalid commands.
- Handle tracking loss.
- Test initially without motion commands.
