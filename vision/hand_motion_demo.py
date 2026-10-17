import cv2
import mediapipe as mp

from hand_motion import HandMotionTracker


def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open webcam.")
        return

    tracker = HandMotionTracker(
        alpha=0.25,
        deadzone=0.015,
    )

    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils

    tracking = False

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
                    break

                frame = cv2.flip(frame, 1)

                rgb = cv2.cvtColor(
                    frame, cv2.COLOR_BGR2RGB
                )

                results = hands.process(rgb)

                dx = 0.0
                dy = 0.0

                if results.multi_hand_landmarks:
                    hand = results.multi_hand_landmarks[0]
                    dx, dy = tracker.update(hand)
                    tracking = True

                    mp_draw.draw_landmarks(
                        frame,
                        hand,
                        mp_hands.HAND_CONNECTIONS
                    )
                else:
                    # Recalibrate after losing tracking.
                    tracker.reset()
                    tracking = False

                status = (
                    "TRACKING"
                    if tracking
                    else "NO HAND"
                )

                cv2.putText(
                    frame,
                    status,
                    (20, 35),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2,
                )

                cv2.putText(
                    frame,
                    f"DX: {dx:+.3f}",
                    (20, 75),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2,
                )

                cv2.putText(
                    frame,
                    f"DY (UP): {dy:+.3f}",
                    (20, 110),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2,
                )

                cv2.putText(
                    frame,
                    "R: Reset reference | Q: Quit",
                    (20, 145),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    1,
                )

                cv2.imshow(
                    "Robot 4R - Hand Motion",
                    frame,
                )

                key = cv2.waitKey(1) & 0xFF

                if key == ord("q"):
                    break

                if key == ord("r"):
                    tracker.reset()
                    print("Reference position reset.")

    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
