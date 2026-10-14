import math

# ==================================
# ROBOT PARAMETERS (meters)
# ==================================

L1 = 0.10  # Base height
L2 = 0.15  # Upper arm
L3 = 0.15  # Forearm
L4 = 0.06  # Wrist / tool

# ==================================
# FORWARD KINEMATICS
# ==================================

def forward_kinematics(q1, q2, q3, q4):

    # Horizontal distance from base axis
    r = (
        L2 * math.cos(q2)
        + L3 * math.cos(q2 + q3)
        + L4 * math.cos(q2 + q3 + q4)
    )

    # Cartesian coordinates
    x = r * math.cos(q1)
    y = r * math.sin(q1)

    z = (
        L1
        + L2 * math.sin(q2)
        + L3 * math.sin(q2 + q3)
        + L4 * math.sin(q2 + q3 + q4)
    )

    return x, y, z


# ==================================
# TEST
# ==================================

if __name__ == "__main__":

    # Joint angles in radians
    q1 = -0.051
    q2 = 0.959
    q3 = -0.097
    q4 = -0.670

    x, y, z = forward_kinematics(q1, q2, q3, q4)

    print("=== ROBOT 4R FK ===")
    print(f"X = {x:.4f} m")
    print(f"Y = {y:.4f} m")
    print(f"Z = {z:.4f} m")
