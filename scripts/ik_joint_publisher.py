import math
import rclpy

from rclpy.node import Node
from sensor_msgs.msg import JointState

from inverse_kinematics import inverse_kinematics


class IKJointPublisher(Node):

    def __init__(self):
        super().__init__('ik_joint_publisher')

        self.publisher = self.create_publisher(
            JointState,
            '/joint_states',
            10
        )

        self.joint_names = [
            'joint1',
            'joint2',
            'joint3',
            'joint4'
        ]

        # Desired position
        x = 0.20
        y = 0.10
        z = 0.15

        # Desired tool pitch
        phi = math.radians(0)

        solutions = inverse_kinematics(
            x, y, z, phi
        )

        if not solutions:
            raise ValueError(
                "No valid IK solution!"
            )

        # Select solution 1
        self.angles = solutions[1]

        self.timer = self.create_timer(
            0.1,
            self.publish_joints
        )

        self.get_logger().info(
            f'IK solution: {self.angles}'
        )

    def publish_joints(self):

        msg = JointState()

        msg.header.stamp = (
            self.get_clock().now().to_msg()
        )

        msg.name = self.joint_names
        msg.position = self.angles

        self.publisher.publish(msg)


def main():

    rclpy.init()

    node = IKJointPublisher()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
