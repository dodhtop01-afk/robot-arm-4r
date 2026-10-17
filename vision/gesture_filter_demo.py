import time

import cv2
import mediapipe as mp

from gesture_recognition import recognize_gesture
from gesture_filter import GestureFilter


def main():

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open webcam.")
        return

    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils

    gesture_filter = GestureFilter(
        confirmation_time=0.25
    )

    previous_time = time.perf_counter()

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

                rgb_frame = cv2.cvtColor(
                    frame,
                    cv2.COLOR_BGR2RGB
                )

                results = hands.process(rgb_frame)

                raw_gesture = "NO HAND"

                if results.multi_hand_landmarks:

                    hand_landmarks = (
                        results.multi_hand_landmarks[0]
                    )

                    raw_gesture = recognize_gesture(
                        hand_landmarks
                    )

                    mp_draw.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS
                    )

                stable_gesture = gesture_filter.update(
                    raw_gesture
                )

                current_time = time.perf_counter()

                fps = 1.0 / max(
                    current_time - previous_time,
                    1e-6
                )

                previous_time = current_time

                cv2.putText(
                    frame,
                    f"RAW: {raw_gesture}",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2
                )

                cv2.putText(
                    frame,
                    f"STABLE: {stable_gesture}",
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"FPS: {fps:.1f}",
                    (20, 120),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2
                )

                cv2.imshow(
                    "Robot 4R - Gesture Stabilization",
                    frame
                )

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
