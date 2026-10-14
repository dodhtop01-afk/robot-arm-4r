# Joint Velocity & Acceleration Constraints

## Objective

Automatically adjust movement duration to satisfy
the configured joint velocity and acceleration limits.

## Trajectory Model

Cubic Smoothstep:

$$
q(t)=q_A+(q_B-q_A)(3u^2-2u^3)
$$

Where:

$$
u=\frac{t}{T}
$$

## Velocity Constraint

$$
|\dot q|_{\max}=\frac{1.5|\Delta q|}{T}
$$

## Acceleration Constraint

$$
|\ddot q|_{\max}=\frac{6|\Delta q|}{T^2}
$$

## Duration Selection

$$
T_{\mathrm{safe}}=
\max\left(
T_{\mathrm{requested}},
\max_i\frac{1.5|\Delta q_i|}{v_{i,\max}},
\max_i\sqrt{\frac{6|\Delta q_i|}{a_{i,\max}}}
\right)
$$

## Simulation Parameters

Maximum joint velocity:

1.0 rad/s

Maximum joint acceleration:

2.0 rad/s²

These values are provisional simulation limits,
not verified hardware specifications.

## Verification

Test A:
Requested duration: 0.10 s
Actual duration: 2.89 s
Result: PASS

Test B:
Requested duration: 8.00 s
Actual duration: 8.00 s
Result: PASS

## Limitations

- No collision checking.
- No motor torque constraints.
- No physical feedback.
- No hardware validation.
- ROS 2 JointState is used for visualization.

## Conclusion

Automatic trajectory duration adjustment
passed the two functional tests.

The kinematic simulation MVP is complete.
