# Inverse Kinematics — Robot 4R

## 1. Objective

Find the joint angles q1, q2, q3, q4 from
a desired end-effector position and pitch.

Input:
- X, Y, Z: Target coordinates (meters)
- Phi: Desired tool pitch (degrees)

Output:
- q1, q2, q3, q4 (radians)

## 2. Robot dimensions

L1 = 0.10 m
L2 = 0.15 m
L3 = 0.15 m
L4 = 0.06 m

## 3. Geometric interpretation

X: Forward/backward position.
Y: Left/right position.
Z: Vertical position.
Phi: Tool inclination relative to the
      horizontal plane of the arm.

## 4. Base rotation

For the standard forward-facing solution:

q1 = atan2(Y, X)

Horizontal distance:

r = sqrt(X² + Y²)

Note:
The FK model uses a signed radial coordinate.
This IK branch assumes r >= 0.

## 5. Wrist center

rw = r - L4*cos(Phi)

zw = Z - L1 - L4*sin(Phi)

These coordinates describe the wrist joint
relative to the shoulder in the arm plane.

## 6. Joint limits

J1: -3.14 to 3.14 rad
J2: -1.57 to 1.57 rad
J3: -2.00 to 2.00 rad
J4: -1.57 to 1.57 rad

A target is valid only if an IK solution
exists and satisfies all joint limits.

## 7. Verification

Target:
X = 0.20 m
Y = 0.10 m
Z = 0.15 m
Phi = 0 degrees

Verified ROS 2 TF translation:
[0.200, 0.100, 0.150] m

## 8. Limitations

- Only the forward-facing base solution
  is currently considered.
- Collision detection is not implemented.
- Joint limits are provisional.
- This is kinematic simulation, not
  physical actuator control.
