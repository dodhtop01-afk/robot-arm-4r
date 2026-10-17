#!/usr/bin/env python3

import argparse
import json
import math
import socket
import sys
import time
from pathlib import Path

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
sys.path.insert(0, str(PROJECT_ROOT / "vision"))

from inverse_kinematics import inverse_kinematics
from workspace_mapping import RobotTarget
from ik_validation import validate_target


HOST = "127.0.0.1"
PORT = 5005

JOINT_NAMES = ["joint1", "joint2", "joint3", "joint4"]

CONTROL_INTERVAL = 0.1
TRAJECTORY_DURATION = 0.3
MAX_JOINT_SPEED = 0.5

TARGET_TIMEOUT = 0.35
FEEDBACK_TIMEOUT = 0.5


class HandROS2Bridge(Node):

    def __init__(self, live=False):
        super().__init__("hand_ros2_bridge")

        self.live = live

        self.publisher = self.create_publisher(
            JointTrajectory,
            "/arm_controller/joint_trajectory",
            10
        )

        self.subscription = self.create_subscription(
            JointState,
            "/joint_states",
            self.joint_callback,
            qos_profile_sensor_data
        )

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((HOST, PORT))
        self.sock.setblocking(False)

        self.actual_angles = None
        self.last_feedback = None

        self.target = None
        self.last_target_time = None
        self.last_sequence = -1

        self.last_control_time = 0.0
        self.timeout_handled = False

        self.get_logger().info(
            f"Bridge started | Mode: {'LIVE' if live else 'DRY RUN'}"
        )

    def joint_callback(self, msg):
        positions = dict(zip(msg.name, msg.position))

        if all(name in positions for name in JOINT_NAMES):
            angles = [positions[name] for name in JOINT_NAMES]

            if all(math.isfinite(q) for q in angles):
                self.actual_angles = angles
                self.last_feedback = time.monotonic()

    def receive_packets(self):
        # Drain queued packets; keep the newest valid target.
        for _ in range(100):
            try:
                data, _ = self.sock.recvfrom(4096)
            except BlockingIOError:
                break

            try:
                packet = json.loads(data.decode("utf-8"))

                if not isinstance(packet, dict):
                    continue

                seq = packet["seq"]

                if type(seq) is not int or seq <= self.last_sequence:
                    continue

                values = [
                    packet["x"],
                    packet["y"],
                    packet["z"],
                    packet["pitch"]
                ]

                if any(type(v) not in (int, float) for v in values):
                    continue

                if not all(math.isfinite(v) for v in values):
                    continue

                x, y, z, pitch = values

                # Enforce the same bounds on the receiving side.
                if not (
                    abs(x - 0.20) < 1e-6
                    and 0.06 <= y <= 0.14
                    and 0.11 <= z <= 0.19
                    and abs(pitch) < 1e-6
                ):
                    continue

                target = RobotTarget(x, y, z, pitch)

                if not validate_target(target).reachable:
                    continue

                self.target = target
                self.last_sequence = seq
                self.last_target_time = time.monotonic()
                self.timeout_handled = False

            except (KeyError, ValueError, TypeError, UnicodeDecodeError):
                continue

    def send_trajectory(self, angles, duration):
        trajectory = JointTrajectory()
        trajectory.joint_names = JOINT_NAMES

        point = JointTrajectoryPoint()
        point.positions = [float(q) for q in angles]
        point.velocities = [0.0] * 4

        seconds = int(duration)
        point.time_from_start.sec = seconds
        point.time_from_start.nanosec = int(
            (duration - seconds) * 1e9
        )

        trajectory.points = [point]
        self.publisher.publish(trajectory)

    def control_step(self):
        now = time.monotonic()

        if now - self.last_control_time < CONTROL_INTERVAL:
            return

        self.last_control_time = now

        if (
            self.actual_angles is None
            or self.last_feedback is None
            or now - self.last_feedback > FEEDBACK_TIMEOUT
        ):
            # Never command motion without fresh joint feedback.
            return

        target_fresh = (
            self.target is not None
            and self.last_target_time is not None
            and now - self.last_target_time <= TARGET_TIMEOUT
        )

        if not target_fresh:
            if not self.timeout_handled:
                self.get_logger().warning(
                    "Target timeout: hold current joint position"
                )

                if self.live:
                    self.send_trajectory(
                        self.actual_angles,
                        0.2
                    )

                self.timeout_handled = True

            return

        target = self.target

        try:
            solutions = inverse_kinematics(
                target.x,
                target.y,
                target.z,
                target.pitch
            )
        except ValueError:
            return

        if not solutions:
            return

        current = self.actual_angles

        # Choose nearest IK configuration.
        goal = min(
            solutions,
            key=lambda solution: sum(
                (a - b) ** 2
                for a, b in zip(solution, current)
            )
        )

        # Limit each joint's commanded displacement.
        max_step = MAX_JOINT_SPEED * CONTROL_INTERVAL

        limited_goal = [
            q + max(-max_step, min(max_step, desired - q))
            for q, desired in zip(current, goal)
        ]

        if self.live:
            self.send_trajectory(
                limited_goal,
                TRAJECTORY_DURATION
            )

        self.get_logger().info(
            f"{'LIVE' if self.live else 'DRY'} | "
            f"XYZ=({target.x:.3f}, {target.y:.3f}, "
            f"{target.z:.3f}) | "
            f"q={[round(q, 3) for q in limited_goal]}"
        )

    def close(self):
        self.sock.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--live",
        action="store_true",
        help="Publish trajectories to Gazebo"
    )

    args = parser.parse_args()

    rclpy.init()
    node = HandROS2Bridge(live=args.live)

    try:
        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=0.01)
            node.receive_packets()
            node.control_step()

    except KeyboardInterrupt:
        pass

    finally:
        node.close()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
