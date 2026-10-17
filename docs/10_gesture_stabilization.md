# PHASE 03 — Step 03: Gesture Stabilization

## Objective

Stabilize hand gesture recognition before using gestures
to control a robotic gripper.

## Method

A time-based confirmation filter is implemented.

Confirmation time:

T_confirm = 0.25 seconds

A new OPEN or FIST gesture must remain continuously
recognized for at least 250 ms before becoming stable.

UNKNOWN and NO HAND do not change the last
confirmed gripper gesture.

## Implementation

Files:

- vision/gesture_filter.py
- vision/gesture_filter_demo.py

## Verification

| Test | Result |
|---|---|
| OPEN recognition | PASS |
| FIST recognition | PASS |
| Quick gesture transitions | PASS |
| UNKNOWN holds previous state | PASS |
| NO HAND holds previous state | PASS |

Observed demo performance: approximately 28–34 FPS.

## Limitations

- Confirmation introduces approximately 250 ms
  of additional response delay.
- Gesture classification can still be affected
  by hand orientation and landmark estimation errors.
- Only a manual functional test has been performed.
- No automatic unit tests have been implemented.
- No ROS 2 or physical gripper integration yet.

## Safety Considerations

The last stable gesture must not be interpreted
as permission to continue moving the robot.

Future integration must separate:

- Gesture state
- Hand tracking validity
- Motion enable/disable state

## Next Step

PHASE 03 — Step 04: Hand Motion Tracking

Track hand displacement and map it into robot
workspace coordinates.
