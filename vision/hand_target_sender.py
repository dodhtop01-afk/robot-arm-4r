import json
import socket
import time

import cv2
import mediapipe as mp

from hand_motion import HandMotionTracker
from workspace_mapping import WorkspaceMapper
from ik_validation import validate_target


HOST = "127.0.0.1"
PORT = 5005

SEND_INTERVAL = 0.1  # 10 Hz


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open webcam.")
        sock.close()
        return

    tracker = HandMotionTracker(alpha=0.25, deadzone=0.015)
    mapper = WorkspaceMapper()

    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils

    last_send = 0.0
    sequence = 0

    try:
        with mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            model_complexity=0,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6,
        ) as hands:

            while True:
                ok, frame = cap.read()
                if not ok:
                    break

                frame = cv2.flip(frame, 1)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(rgb)

                now = time.monotonic()
                status = "NO HAND"

                if results.multi_hand_landmarks:
                    hand = results.multi_hand_landmarks[0]
                    dx, dy = tracker.update(hand)

                    target = mapper.map(dx, dy)
                    validation = validate_target(target)

                    status = (
                        "REACHABLE"
                        if validation.reachable
                        else "UNREACHABLE"
                    )

                    if (
                        validation.reachable
                        and now - last_send >= SEND_INTERVAL
                    ):
                        packet = {
                            "seq": sequence,
                            "x": target.x,
                            "y": target.y,
                            "z": target.z,
                            "pitch": target.pitch,
                        }

                        sock.sendto(
                            json.dumps(packet).encode("utf-8"),
                            (HOST, PORT),
                        )

                        sequence += 1
                        last_send = now

                    mp_draw.draw_landmarks(
                        frame,
                        hand,
                        mp_hands.HAND_CONNECTIONS,
                    )
                else:
                    tracker.reset()

                cv2.putText(
                    frame,
                    f"VISION: {status}",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2,
                )

                cv2.putText(
                    frame,
                    "Q: Quit | R: Reset",
                    (20, 75),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2,
                )

                cv2.imshow("Robot 4R - Vision Sender", frame)

                key = cv2.waitKey(1) & 0xFF

                if key == ord("q"):
                    break
                if key == ord("r"):
                    tracker.reset()

    finally:
        cap.release()
        cv2.destroyAllWindows()
        sock.close()


if __name__ == "__main__":
    main()
