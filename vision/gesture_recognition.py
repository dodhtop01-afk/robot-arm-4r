import math


# MCP, PIP, TIP for index, middle, ring, pinky
FINGER_JOINTS = [
    (5, 6, 8),
    (9, 10, 12),
    (13, 14, 16),
    (17, 18, 20),
]


def calculate_angle(a, b, c):
    """
    Calculate the angle ABC in degrees.
    """

    ba = (
        a.x - b.x,
        a.y - b.y,
        a.z - b.z,
    )

    bc = (
        c.x - b.x,
        c.y - b.y,
        c.z - b.z,
    )

    dot_product = sum(
        x * y for x, y in zip(ba, bc)
    )

    norm_ba = math.sqrt(
        sum(x * x for x in ba)
    )

    norm_bc = math.sqrt(
        sum(x * x for x in bc)
    )

    if norm_ba < 1e-8 or norm_bc < 1e-8:
        return None

    cos_angle = dot_product / (norm_ba * norm_bc)

    cos_angle = max(-1.0, min(1.0, cos_angle))

    return math.degrees(math.acos(cos_angle))


def recognize_gesture(hand_landmarks):

    landmarks = hand_landmarks.landmark

    extended_count = 0
    folded_count = 0

    for mcp, pip, tip in FINGER_JOINTS:

        angle = calculate_angle(
            landmarks[mcp],
            landmarks[pip],
            landmarks[tip],
        )

        if angle is None:
            return "UNKNOWN"

        if angle > 160:
            extended_count += 1

        elif angle < 110:
            folded_count += 1

    if extended_count == 4:
        return "OPEN"

    if folded_count == 4:
        return "FIST"

    return "UNKNOWN"
