import math
import sys
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from inverse_kinematics import inverse_kinematics
from forward_kinematics import forward_kinematics


@dataclass(frozen=True)
class IKResult:
    reachable: bool
    angles: tuple | None
    error: float | None
    reason: str


def validate_target(target):
    """
    Validate a Cartesian target using the existing IK.

    This function does not command robot motion.
    """

    values = (
        target.x,
        target.y,
        target.z,
        target.pitch,
    )

    if not all(math.isfinite(v) for v in values):
        return IKResult(
            False, None, None, "Non-finite target"
        )

    try:
        solutions = inverse_kinematics(
            target.x,
            target.y,
            target.z,
            target.pitch,
        )

    except ValueError as exc:
        return IKResult(
            False, None, None, str(exc)
        )

    if not solutions:
        return IKResult(
            False,
            None,
            None,
            "No IK solution within joint limits",
        )

    # Use the first valid IK configuration for this demo.
    angles = tuple(solutions[0])

    x_fk, y_fk, z_fk = forward_kinematics(*angles)

    error = math.sqrt(
        (target.x - x_fk) ** 2
        + (target.y - y_fk) ** 2
        + (target.z - z_fk) ** 2
    )

    if not math.isfinite(error) or error > 1e-5:
        return IKResult(
            False,
            None,
            error,
            "FK verification failed",
        )

    return IKResult(
        True,
        angles,
        error,
        "Valid IK solution",
    )
