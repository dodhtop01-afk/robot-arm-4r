import math
from forward_kinematics import forward_kinematics

# Robot dimensions (meters)
L1 = 0.10
L2 = 0.15
L3 = 0.15
L4 = 0.06

# Joint limits (radians), matching our URDF
JOINT_LIMITS = [
    (-3.14, 3.14),
    (-1.57, 1.57),
    (-2.0, 2.0),
    (-1.57, 1.57)
]


def inverse_kinematics(x, y, z, phi):

    # STEP 1: Base rotation
    q1 = math.atan2(y, x)

    # Horizontal distance to target
    r = math.hypot(x, y)

    # STEP 2: Wrist center
    rw = r - L4 * math.cos(phi)
    zw = z - L1 - L4 * math.sin(phi)

    # STEP 3: Elbow angle using cosine law
    D = (rw**2 + zw**2 - L2**2 - L3**2) / (2 * L2 * L3)

    if D < -1.000001 or D > 1.000001:
        raise ValueError("Target is outside the 2R workspace")

    D = max(-1.0, min(1.0, D))

    solutions = []

    # Two possible elbow configurations
    for sign in [1, -1]:

        q3 = math.atan2(sign * math.sqrt(1 - D**2), D)

        # STEP 4: Shoulder angle
        q2 = (
            math.atan2(zw, rw)
            - math.atan2(
                L3 * math.sin(q3),
                L2 + L3 * math.cos(q3)
            )
        )

        # STEP 5: Wrist angle
        q4 = phi - q2 - q3

        angles = [q1, q2, q3, q4]

        # Check joint limits
        valid = all(
            lower <= angle <= upper
            for angle, (lower, upper) in zip(
                angles, JOINT_LIMITS
            )
        )

        if valid:
            solutions.append(angles)

    return solutions


if __name__ == "__main__":

    # Desired end-effector position
    x_target = 0.20
    y_target = 0.10
    z_target = 0.15

    # Desired tool pitch
    phi = math.radians(0)

    solutions = inverse_kinematics(
        x_target, y_target, z_target, phi
    )

    if not solutions:
        print("No valid IK solution within joint limits.")

    for i, angles in enumerate(solutions, start=1):

        print(f"\n=== IK SOLUTION {i} ===")

        for j, angle in enumerate(angles, start=1):
            print(
                f"q{j} = {angle:.4f} rad "
                f"({math.degrees(angle):.2f} deg)"
            )

        # Validate using Forward Kinematics
        x_fk, y_fk, z_fk = forward_kinematics(*angles)

        error = math.sqrt(
            (x_target - x_fk)**2
            + (y_target - y_fk)**2
            + (z_target - z_fk)**2
        )

        print("\nFK verification:")
        print(f"X = {x_fk:.4f} m")
        print(f"Y = {y_fk:.4f} m")
        print(f"Z = {z_fk:.4f} m")
        print(f"Position error = {error:.8f} m")
