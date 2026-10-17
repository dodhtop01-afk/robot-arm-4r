# PHASE 03 — Step 02: Hand Gesture Recognition

## Objective

Recognize hand gestures using MediaPipe hand landmarks.

Supported gestures:
- OPEN
- FIST
- UNKNOWN

## Method

The system uses 3D landmark coordinates to calculate
finger joint angles.

For three points A, B, C:

cos(theta) = dot(BA, BC) / (|BA| * |BC|)

Four fingers are evaluated:
- Index
- Middle
- Ring
- Pinky

Classification rules:

- OPEN: All four fingers extended (>160 degrees).
- FIST: All four fingers folded (<110 degrees).
- UNKNOWN: Other configurations.

The thumb is not currently evaluated.

## Implementation

Files:

- vision/gesture_recognition.py
- vision/gesture_demo.py

## Verification

| Gesture | Expected | Observed |
|---|---|---|
| Open palm | OPEN | PASS |
| Closed fist | FIST | PASS |
| Two fingers | UNKNOWN | PASS |

Observed performance: approximately 25–33 FPS.

## Limitations

- Thresholds are experimental.
- Recognition may change with hand orientation.
- No temporal filtering.
- No confidence-based gesture stabilization.
- The thumb is not included.
- Tests have only verified individual gesture examples.

## Next Step

Implement temporal filtering to prevent rapid switching
between gesture states.

The resulting stable gestures will later control
the robot gripper.
