import math
import tkinter as tk
from tkinter import ttk

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from sensor_msgs.msg import JointState
from trajectory_msgs.msg import (
    JointTrajectory,
    JointTrajectoryPoint,
)

from inverse_kinematics import inverse_kinematics
from forward_kinematics import forward_kinematics


class IKControlGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Robot 4R - Gazebo IK Controller")
        self.root.geometry("420x540")

        # ROS 2
        rclpy.init()
        self.node = Node("gazebo_ik_control_gui")

        self.joint_names = [
            "joint1", "joint2", "joint3", "joint4"
        ]

        # Send trajectories to the controller
        self.publisher = self.node.create_publisher(
            JointTrajectory,
            "/arm_controller/joint_trajectory",
            10
        )

        # Receive actual joint states from Gazebo
        self.subscription = self.node.create_subscription(
            JointState,
            "/joint_states",
            self.joint_state_callback,
            qos_profile_sensor_data
        )

        self.angles = [0.0] * 4
        self.have_joint_states = False
        self.running = True

        # Simulation motion limits
        self.max_velocity = [1.0] * 4
        self.max_acceleration = [2.0] * 4

        self.entries = {}

        defaults = {
            "X (m)": "0.20",
            "Y (m)": "0.10",
            "Z (m)": "0.15",
            "Pitch (deg)": "0",
            "Move Duration (s)": "2.0"
        }

        title = ttk.Label(
            root,
            text="ROBOT 4R | GAZEBO IK",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=15)

        for label, value in defaults.items():
            frame = ttk.Frame(root)
            frame.pack(fill="x", padx=30, pady=5)

            ttk.Label(
                frame, text=label, width=18
            ).pack(side="left")

            entry = ttk.Entry(frame, width=14)
            entry.insert(0, value)
            entry.pack(side="right")

            self.entries[label] = entry

        ttk.Label(
            root, text="IK Configuration"
        ).pack(pady=(15, 5))

        self.solution_mode = tk.StringVar(value="Auto")

        ttk.Combobox(
            root,
            textvariable=self.solution_mode,
            values=["Auto", "1", "2"],
            state="readonly",
            width=10
        ).pack()

        ttk.Button(
            root,
            text="Calculate & Move",
            command=self.move_robot
        ).pack(pady=15)

        ttk.Button(
            root,
            text="Home Position",
            command=self.home_robot
        ).pack()

        self.result_label = ttk.Label(
            root,
            text="Waiting for Gazebo joint states...",
            font=("Courier", 11),
            justify="left"
        )
        self.result_label.pack(pady=15)

        self.status = tk.StringVar(
            value="Waiting for /joint_states..."
        )

        ttk.Label(
            root,
            textvariable=self.status,
            wraplength=370
        ).pack(pady=5)

        self.root.protocol(
            "WM_DELETE_WINDOW", self.close
        )

        # Process ROS callbacks using Tkinter
        self.process_ros()

    def joint_state_callback(self, msg):
        """
        Read actual joint angles from Gazebo.

        JointState ordering is not guaranteed.
        Always match positions by joint name.
        """

        positions = dict(zip(msg.name, msg.position))

        if not all(
            name in positions
            for name in self.joint_names
        ):
            return

        angles = [
            positions[name]
            for name in self.joint_names
        ]

        if not all(math.isfinite(q) for q in angles):
            return

        self.angles = angles
        self.update_result()

        if not self.have_joint_states:
            self.have_joint_states = True
            self.status.set("Connected to Gazebo.")

    def select_ik_solution(self, solutions):

        mode = self.solution_mode.get()

        if mode == "Auto":
            return min(
                solutions,
                key=lambda solution: math.dist(
                    self.angles, solution
                )
            )

        index = int(mode) - 1

        if index < 0 or index >= len(solutions):
            raise ValueError(
                f"Only {len(solutions)} valid IK solution(s)."
            )

        return solutions[index]

    def calculate_safe_duration(
        self,
        start_angles,
        target_angles,
        requested_duration
    ):

        duration = requested_duration

        for i in range(4):
            delta = abs(
                target_angles[i] - start_angles[i]
            )

            t_velocity = (
                1.5 * delta / self.max_velocity[i]
            )

            t_acceleration = math.sqrt(
                6.0 * delta / self.max_acceleration[i]
            )

            duration = max(
                duration,
                t_velocity,
                t_acceleration
            )

        return duration

    def send_trajectory(
        self,
        target_angles,
        requested_duration
    ):

        if not self.have_joint_states:
            self.status.set(
                "No joint feedback from Gazebo."
            )
            return

        start_angles = self.angles.copy()

        duration = self.calculate_safe_duration(
            start_angles,
            target_angles,
            requested_duration
        )

        # Generate Smoothstep waypoints at ~20 Hz
        steps = max(2, math.ceil(duration * 20))

        trajectory = JointTrajectory()
        trajectory.joint_names = self.joint_names

        for k in range(steps + 1):

            u = k / steps
            t = u * duration

            # Cubic Smoothstep
            s = 3 * u**2 - 2 * u**3

            # First derivative with respect to time
            ds_dt = (6 * u - 6 * u**2) / duration

            point = JointTrajectoryPoint()

            point.positions = [
                start + s * (target - start)
                for start, target in zip(
                    start_angles,
                    target_angles
                )
            ]

            point.velocities = [
                ds_dt * (target - start)
                for start, target in zip(
                    start_angles,
                    target_angles
                )
            ]

            # Time from trajectory start
            total_ns = round(t * 1_000_000_000)

            point.time_from_start.sec = (
                total_ns // 1_000_000_000
            )

            point.time_from_start.nanosec = (
                total_ns % 1_000_000_000
            )

            trajectory.points.append(point)

        self.publisher.publish(trajectory)

        self.status.set(
            f"Trajectory sent | "
            f"Requested: {requested_duration:.2f}s | "
            f"Actual: {duration:.2f}s"
        )

    def move_robot(self):

        try:
            if not self.have_joint_states:
                raise ValueError(
                    "Waiting for Gazebo joint feedback."
                )

            x = float(self.entries["X (m)"].get())
            y = float(self.entries["Y (m)"].get())
            z = float(self.entries["Z (m)"].get())
            pitch = float(
                self.entries["Pitch (deg)"].get()
            )

            duration = float(
                self.entries["Move Duration (s)"].get()
            )

            if not all(
                math.isfinite(v)
                for v in [x, y, z, pitch, duration]
            ):
                raise ValueError(
                    "Inputs must be finite numbers."
                )

            if duration <= 0 or duration > 120:
                raise ValueError(
                    "Duration must be between 0 and 120 s."
                )

            phi = math.radians(pitch)

            solutions = inverse_kinematics(
                x, y, z, phi
            )

            if not solutions:
                self.status.set(
                    "No valid IK solution."
                )
                return

            target = self.select_ik_solution(
                solutions
            )

            # Verify IK using FK
            fx, fy, fz = forward_kinematics(
                *target
            )

            error = math.dist(
                [x, y, z],
                [fx, fy, fz]
            )

            if error > 1e-5:
                self.status.set(
                    "FK verification failed."
                )
                return

            self.send_trajectory(
                target,
                duration
            )

        except ValueError as e:
            self.status.set(f"Invalid target: {e}")

    def home_robot(self):
        self.send_trajectory(
            [0.0] * 4,
            3.0
        )

    def update_result(self):

        degrees = [
            math.degrees(q)
            for q in self.angles
        ]

        text = "ACTUAL JOINT ANGLES\n\n"

        text += "\n".join(
            f"J{i+1}: {angle:8.2f}°"
            for i, angle in enumerate(degrees)
        )

        self.result_label.config(text=text)

    def process_ros(self):
        """
        Process ROS callbacks without blocking Tkinter.
        """

        if not self.running:
            return

        rclpy.spin_once(
            self.node,
            timeout_sec=0.0
        )

        self.root.after(
            20,
            self.process_ros
        )

    def close(self):

        self.running = False

        self.node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()

        self.root.destroy()


if __name__ == "__main__":

    root = tk.Tk()

    app = IKControlGUI(root)

    root.mainloop()
