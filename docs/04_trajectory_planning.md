# Joint-Space Trajectory Planning

## 1. Objective

Move the robot smoothly between two
joint configurations.

Instead of instantly changing joint angles,
generate intermediate configurations.

## 2. Trajectory equation

q(t) = q_start + s(u)*(q_target - q_start)

Where:

u = t/T

t: Elapsed time
T: Total movement duration
u: Normalized time (0 to 1)

## 3. Cubic Smoothstep

s(u) = 3u² - 2u³

Boundary conditions:

s(0) = 0
s(1) = 1

s'(0) = 0
s'(1) = 0

These conditions ensure that the
trajectory starts and ends with zero velocity.

## 4. Why use a cubic polynomial?

Assume:

s(u) = au³ + bu² + cu + d

Applying the four boundary conditions:

d = 0
c = 0
a + b = 1
3a + 2b = 0

Therefore:

a = -2
b = 3

Result:

s(u) = 3u² - 2u³

## 5. Implementation

File:
scripts/ik_control_gui.py

Trajectory updates:
10 Hz

Time measurement:
time.monotonic()

## 6. Current limitations

- Joint-space interpolation only.
- No Cartesian straight-line guarantee.
- No automatic velocity/acceleration
  limit enforcement.
- No collision avoidance.
- RViz2 visualization, not motor control.

## 7. Verification

GUI displays:
"Trajectory completed."

Movement durations tested:
8 seconds.

Smooth motion should be verified visually
and later using recorded joint states.
