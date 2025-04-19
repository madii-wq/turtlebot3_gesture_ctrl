#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String

# Constants for velocity limits and increments
LINEAR_VEL_LIMIT = 0.22  # m/s
ANGULAR_VEL_LIMIT = 2.84  # rad/s
LINEAR_VEL_INCREMENT = 0.05  # m/s
ANGULAR_VEL_INCREMENT = 0.2  # rad/s

class CmdVelPublisher(Node):
    def __init__(self):
        super().__init__('turtlebot3_cmd_vel')
        
        # Initialize variables
        self.position = 'Stop'
        self.linear_vel = 0.0
        self.angular_vel = 0.0

        # Create publisher for cmd_vel
        self.cmd_vel_publisher = self.create_publisher(
            Twist, 
            "/cmd_vel", 
            10
        )
        self.get_logger().info("CMD_VEL publisher created!")

        # Create subscription to chatter topic
        self.subscription = self.create_subscription(
            String,
            "chatter",
            self.listener_callback,
            10
        )
        self.get_logger().info("Listening to chatter topic...")

        # Create timer for control loop
        self.create_timer(0.1, self.control_loop)

    def listener_callback(self, msg):
        """Callback for processing incoming String messages."""
        new_position = msg.data.strip()
        if new_position != self.position:
            self.get_logger().info(f"New position command: {new_position}")
            self.position = new_position

    def control_loop(self):
        """Main control loop that publishes velocity commands."""
        cmd_msg = Twist()
        
        # Handle position commands
        if self.position == 'Forward':
            self.linear_vel = min(self.linear_vel + LINEAR_VEL_INCREMENT, LINEAR_VEL_LIMIT)
            self.angular_vel = 0.0
        elif self.position == 'Backward':
            self.linear_vel = max(self.linear_vel - LINEAR_VEL_INCREMENT, -LINEAR_VEL_LIMIT)
            self.angular_vel = 0.0
        elif self.position == 'Left':
            self.angular_vel = min(self.angular_vel + ANGULAR_VEL_INCREMENT, ANGULAR_VEL_LIMIT)
            self.linear_vel = 0.0
        elif self.position == 'Right':
            self.angular_vel = max(self.angular_vel - ANGULAR_VEL_INCREMENT, -ANGULAR_VEL_LIMIT)
            self.linear_vel = 0.0
        elif self.position == 'Stop':
            self.linear_vel = 0.0
            self.angular_vel = 0.0

        # Set velocity values
        cmd_msg.linear.x = self.linear_vel
        cmd_msg.angular.z = self.angular_vel  # Fixed: Changed from angular.x to angular.z

        # Publish command
        self.cmd_vel_publisher.publish(cmd_msg)
        self.get_logger().debug(
            f"Publishing - Linear: {self.linear_vel:.2f} m/s, Angular: {self.angular_vel:.2f} rad/s"
        )

def main(args=None):
    rclpy.init(args=args)
    cmd_vel_publisher = CmdVelPublisher()
    
    try:
        rclpy.spin(cmd_vel_publisher)
    except KeyboardInterrupt:
        cmd_vel_publisher.get_logger().info("Shutting down...")
    finally:
        # Stop the robot before shutting down
        cmd_vel_publisher.cmd_vel_publisher.publish(Twist())
        cmd_vel_publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()