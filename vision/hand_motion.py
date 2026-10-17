class HandMotionTracker:
    """
    Track normalized hand displacement relative
    to a reference position.
    """

    def __init__(self, alpha=0.25, deadzone=0.015):
        if not 0.0 < alpha <= 1.0:
            raise ValueError("alpha must be in (0, 1]")

        if deadzone < 0.0:
            raise ValueError("deadzone must be non-negative")

        self.alpha = alpha
        self.deadzone = deadzone

        self.reference = None
        self.filtered = None

    def reset(self):
        self.reference = None
        self.filtered = None

    def update(self, hand_landmarks):
        landmarks = hand_landmarks.landmark

        wrist = landmarks[0]
        middle_mcp = landmarks[9]

        x = (wrist.x + middle_mcp.x) / 2.0
        y = (wrist.y + middle_mcp.y) / 2.0

        if self.reference is None:
            self.reference = (x, y)
            self.filtered = (x, y)

        else:
            fx, fy = self.filtered

            fx = self.alpha * x + (1 - self.alpha) * fx
            fy = self.alpha * y + (1 - self.alpha) * fy

            self.filtered = (fx, fy)

        fx, fy = self.filtered
        x0, y0 = self.reference

        dx = fx - x0
        dy = y0 - fy

        if abs(dx) < self.deadzone:
            dx = 0.0

        if abs(dy) < self.deadzone:
            dy = 0.0

        return dx, dy
