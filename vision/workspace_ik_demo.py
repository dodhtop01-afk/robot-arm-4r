import cv2
import mediapipe as mp

from hand_motion import HandMotionTracker
from workspace_mapping import WorkspaceMapper
from ik_validation import validate_target


def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open webcam.")
        return

    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils

    tracker = HandMotionTracker(
        alpha=0.25,
        deadzone=0.015,
    )

    mapper = WorkspaceMapper()

    try:
        with mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            model_complexity=0,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6,
        ) as hands:

            while True:
                success, frame = cap.read()

                if not success:
                    print("Camera read failed.")
                    break

                frame = cv2.flip(frame, 1)

                rgb = cv2.cvtColor(
                    frame, cv2.COLOR_BGR2RGB
                )

                results = hands.process(rgb)

                lines = []

                if results.multi_hand_landmarks:
                    hand = results.multi_hand_landmarks[0]

                    dx, dy = tracker.update(hand)

                    target = mapper.map(dx, dy)
                    result = validate_target(target)

                    status = (
                        "REACHABLE"
                        if result.reachable
                        else "UNREACHABLE"
                    )

                    lines = [
                        "TRACKING: ACTIVE",
                        f"DX: {dx:+.3f}  DY: {dy:+.3f}",
                        (
                            f"TARGET: X={target.x:.3f} "
                            f"Y={target.y:.3f} "
                            f"Z={target.z:.3f}"
                        ),
                        f"IK: {status}",
                    ]

                    mp_draw.draw_landmarks(
                        frame,
                        hand,
                        mp_hands.HAND_CONNECTIONS,
                    )

                else:
                    tracker.reset()

                    lines = [
                        "TRACKING: NO HAND",
                        "IK: INACTIVE",
                    ]

                for index, line in enumerate(lines):
                    cv2.putText(
                        frame,
                        line,
                        (15, 35 + index * 35),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.55,
                        (255, 255, 255),
                        2,
                    )

                cv2.putText(
                    frame,
                    "R: Reset | Q: Quit",
                    (15, 195),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    1,
                )

                cv2.imshow(
                    "Robot 4R - Workspace IK Validation",
                    frame,
                )

                key = cv2.waitKey(1) & 0xFF

                if key == ord("q"):
                    break

                if key == ord("r"):
                    tracker.reset()

    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
