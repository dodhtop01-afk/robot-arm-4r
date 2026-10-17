from dataclasses import dataclass


@dataclass(frozen=True)
class RobotTarget:
    x: float
    y: float
    z: float
    pitch: float


class WorkspaceMapper:
    """
    Map normalized hand displacement
    to a candidate robot Cartesian target.

    This module does not command robot motion.
    """

    def __init__(
        self,
        x0=0.20,
        y0=0.10,
        z0=0.15,
        gain_y=0.08,
        gain_z=0.08,
        y_limits=(0.06, 0.14),
        z_limits=(0.11, 0.19),
    ):
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0

        self.gain_y = gain_y
        self.gain_z = gain_z

        self.y_limits = y_limits
        self.z_limits = z_limits

    @staticmethod
    def clamp(value, lower, upper):
        return max(lower, min(value, upper))

    def map(self, dx, dy):
        """
        dx: normalized horizontal hand displacement
        dy: normalized upward hand displacement
        """

        y = self.y0 + self.gain_y * dx
        z = self.z0 + self.gain_z * dy

        y = self.clamp(
            y,
            self.y_limits[0],
            self.y_limits[1],
        )

        z = self.clamp(
            z,
            self.z_limits[0],
            self.z_limits[1],
        )

        return RobotTarget(
            x=self.x0,
            y=y,
            z=z,
            pitch=0.0,
        )
