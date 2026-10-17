import time


class GestureFilter:
    """
    Stabilize raw hand gestures using
    time-based confirmation.
    """

    def __init__(self, confirmation_time=0.25):

        self.confirmation_time = confirmation_time

        self.stable_gesture = "UNKNOWN"

        self.candidate_gesture = None
        self.candidate_start_time = None

    def update(self, raw_gesture):

        current_time = time.monotonic()

        # UNKNOWN and NO HAND do not change
        # the last confirmed command.
        if raw_gesture not in ("OPEN", "FIST"):

            self.candidate_gesture = None
            self.candidate_start_time = None

            return self.stable_gesture

        # No transition is required.
        if raw_gesture == self.stable_gesture:

            self.candidate_gesture = None
            self.candidate_start_time = None

            return self.stable_gesture

        # A new gesture may be starting.
        if raw_gesture != self.candidate_gesture:

            self.candidate_gesture = raw_gesture
            self.candidate_start_time = current_time

            return self.stable_gesture

        # Check how long the gesture has remained.
        elapsed = current_time - self.candidate_start_time

        if elapsed >= self.confirmation_time:

            self.stable_gesture = raw_gesture

            self.candidate_gesture = None
            self.candidate_start_time = None

        return self.stable_gesture
