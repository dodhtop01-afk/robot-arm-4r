# Automatic IK Solution Selection

## 1. Objective

Automatically select the IK solution closest
to the robot's current joint configuration.

This reduces unnecessary joint movements
when multiple IK solutions exist.

## 2. Mathematical Principle

Current joint configuration:

q_current = [q1, q2, q3, q4]

Candidate IK solutions:

q_A = [q1A, q2A, q3A, q4A]
q_B = [q1B, q2B, q3B, q4B]

Distance between configurations:

$$
d_i = \sqrt{\sum_{j=1}^{4}
(q_{ij}-q_{current,j})^2}
$$

Select:

$$
q_{best} = \arg\min_{q_i} d_i
$$

## 3. Implementation

File:
scripts/ik_control_gui.py

Function:
select_ik_solution()

Python method:
math.dist()

Available modes:
- Auto
- Solution 1
- Solution 2

## 4. Verification

Test 1:
Manually select IK solution 2.

Result:
Robot reaches solution 2.

Test 2:
Switch to Auto with the same target.

Result:
Robot maintains the current configuration.

Test 3:
Change target X from 0.20 to 0.21 m.

Result:
Auto selects the nearby configuration
without an unnecessary elbow flip.

All three tests passed.

## 5. Limitations

- Uses Euclidean distance in joint space.
- Does not check collisions.
- Does not guarantee a safe trajectory.
- Does not account for motor torque.
- Assumes the current joint angles are known.

## 6. Next Step

Evaluate joint velocity and acceleration limits
before integrating physical actuators.
