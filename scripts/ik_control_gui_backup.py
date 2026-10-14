import math
import tkinter as tk
from tkinter import ttk

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

from inverse_kinematics import inverse_kinematics
from forward_kinematics import forward_kinematics


class IKControlGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Robot 4R - IK Controller")
        self.root.geometry("400x510")

        # ROS 2 publisher
        rclpy.init()
        self.node = Node("ik_control_gui")

        self.publisher = self.node.create_publisher(
            JointState, "/joint_states", 10
        )

        self.joint_names = [
            "joint1", "joint2", "joint3", "joint4"
        ]

        self.angles = [0.0] * 4
        self.running = True

        # Target inputs
        self.entries = {}
        defaults = {
            "X (m)": "0.20",
            "Y (m)": "0.10",
            "Z (m)": "0.15",
            "Pitch (deg)": "0"
        }

        title = ttk.Label(
            root,
            text="ROBOT 4R | IK CONTROL",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=15)

        for label, value in defaults.items():
            frame = ttk.Frame(root)
            frame.pack(fill="x", padx=30, pady=5)

            ttk.Label(
                frame, text=label, width=15
            ).pack(side="left")

            entry = ttk.Entry(frame, width=15)
            entry.insert(0, value)
            entry.pack(side="right")

            self.entries[label] = entry

        # IK solution selection
        ttk.Label(
            root, text="IK Configuration"
        ).pack(pady=(15, 5))

        self.solution_mode = tk.StringVar(value="1")

        ttk.Combobox(
            root,
            textvariable=self.solution_mode,
            values=["1", "2"],
            state="readonly",
            width=10
        ).pack()

        # Control buttons
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

        # Joint results
        self.result_label = ttk.Label(
            root,
            text="J1: 0.00°\nJ2: 0.00°\nJ3: 0.00°\nJ4: 0.00°",
            font=("Courier", 12),
            justify="left"
        )
        self.result_label.pack(pady=15)

        self.status = tk.StringVar(value="Ready")

        ttk.Label(
            root,
            textvariable=self.status,
            wraplength=350
        ).pack(pady=5)

        self.root.protocol(
            "WM_DELETE_WINDOW", self.close
        )

        # Publish at 10 Hz
        self.publish_joints()

    def move_robot(self):
        try:
            x = float(self.entries["X (m)"].get())
            y = float(self.entries["Y (m)"].get())
            z = float(self.entries["Z (m)"].get())
            pitch = float(
                self.entries["Pitch (deg)"].get()
            )

            if not all(
                math.isfinite(v)
                for v in [x, y, z, pitch]
            ):
                raise ValueError("Inputs must be finite numbers.")

            phi = math.radians(pitch)

            solutions = inverse_kinematics(
                x, y, z, phi
            )

            if not solutions:
                self.status.set(
                    "No valid IK solution within joint limits."
                )
                return

            index = int(self.solution_mode.get()) - 1

            if index >= len(solutions):
                self.status.set(
                    f"Only {len(solutions)} valid solution(s). "
                    "Try another configuration."
                )
                return

            new_angles = solutions[index]

            # Verify with FK before publishing
            fx, fy, fz = forward_kinematics(
                *new_angles
            )

            error = math.dist(
                [x, y, z], [fx, fy, fz]
            )

            if error > 1e-5:
                self.status.set("FK verification failed.")
                return

            self.angles = new_angles
            self.update_result()

            self.status.set(
                f"Pose published | FK error: {error:.8f} m"
            )

        except ValueError as e:
            self.status.set(f"Invalid target: {e}")

    def update_result(self):
        degrees = [
            math.degrees(q) for q in self.angles
        ]

        text = "\n".join(
            f"J{i+1}: {angle:8.2f}°"
            for i, angle in enumerate(degrees)
        )

        self.result_label.config(text=text)

    def home_robot(self):
        self.angles = [0.0] * 4
        self.update_result()
        self.status.set("Home pose published")

    def publish_joints(self):
        if not self.running:
            return

        msg = JointState()
        msg.header.stamp = (
            self.node.get_clock().now().to_msg()
        )

        msg.name = self.joint_names
        msg.position = self.angles.copy()

        self.publisher.publish(msg)

        self.root.after(100, self.publish_joints)

    def close(self):
        self.running = False
        self.node.destroy_node()
        rclpy.shutdown()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = IKControlGUI(root)
    root.mainloop()
