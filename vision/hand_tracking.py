import time

import cv2
import mediapipe as mp


def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open webcam. Try camera index 1.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils

    previous_time = time.perf_counter()

    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        model_complexity=0,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6,
    ) as hands:

        while cap.isOpened():
            success, frame = cap.read()

            if not success:
                print("Failed to read camera frame.")
                break

            # Mirror image for intuitive hand movement
            frame = cv2.flip(frame, 1)

            # MediaPipe uses RGB images
            rgb_frame = cv2.cvtColor(
                frame, cv2.COLOR_BGR2RGB
            )

            results = hands.process(rgb_frame)

            hand_detected = False

            if results.multi_hand_landmarks:
                hand_detected = True

                for hand_landmarks in results.multi_hand_landmarks:
                    mp_draw.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                    )

            current_time = time.perf_counter()
            fps = 1.0 / max(
                current_time - previous_time, 1e-6
            )
            previous_time = current_time

            status = (
                "HAND DETECTED"
                if hand_detected
                else "NO HAND"
            )

            cv2.putText(
                frame,
                status,
                (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0) if hand_detected else (0, 0, 255),
                2,
            )

            cv2.putText(
                frame,
                f"FPS: {fps:.1f}",
                (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
            )

            cv2.imshow("Robot 4R - Hand Tracking", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
