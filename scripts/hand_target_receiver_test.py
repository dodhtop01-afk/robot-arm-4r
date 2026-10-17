import json
import socket
import time


HOST = "127.0.0.1"
PORT = 5005


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    sock.settimeout(0.5)

    print(f"Listening for hand targets on {HOST}:{PORT}")

    last_packet_time = None

    try:
        while True:
            try:
                data, address = sock.recvfrom(4096)

                packet = json.loads(data.decode("utf-8"))

                required = ("seq", "x", "y", "z", "pitch")

                if not all(key in packet for key in required):
                    print("Invalid packet: missing fields")
                    continue

                last_packet_time = time.monotonic()

                print(
                    f"SEQ={packet['seq']:4d} | "
                    f"X={packet['x']:.3f} "
                    f"Y={packet['y']:.3f} "
                    f"Z={packet['z']:.3f} | "
                    f"Pitch={packet['pitch']:.3f}"
                )

            except socket.timeout:
                if last_packet_time is not None:
                    if time.monotonic() - last_packet_time > 1.0:
                        print("No recent targets — sender inactive")
                        last_packet_time = None

    except KeyboardInterrupt:
        print("\nReceiver stopped.")

    finally:
        sock.close()


if __name__ == "__main__":
    main()
