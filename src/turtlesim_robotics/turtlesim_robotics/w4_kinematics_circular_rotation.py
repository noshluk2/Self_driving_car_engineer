"""

--> Kinematic Modeling Implementation for differential Drive Robot
- This node contains kinematics Implementation
- Which is going to be driven through a velocity or acceleration controller
- Circular Trajectory is going to be followed
- Errors are going to be calculated using Derivates

10/11/21
Author :
M.Luqman

"""
import rclpy
from rclpy.node import Node
from math import sin, cos 
import time
from sympy import *
from geometry_msgs.msg import Twist, Pose


def get_turtlesim_pose(data):
    global bot_angle
    # bot_pose.x=data.x
    # bot_pose.y=data.y
    bot_angle=data.theta

def send_turtlesim_cmd_vel():
    global bot_angle , publisher , desired_pose,robot_velocity,time_a

    dt = time.time()-time_a
    time_start = time.time()

    robot_angular_velocity_theta = bot_angle

    kinematic_model = Matrix([
        [cos(robot_angular_velocity_theta), -robot_velocity *        sin(robot_angular_velocity_theta)],
        [sin(robot_angular_velocity_theta), robot_velocity  *        cos(robot_angular_velocity_theta)]

    ])
    reference_coordinates = Matrix([ [-sin(time_start)], [-cos(time_start)]   ] )
    acceleration_controller = kinematic_model.inv() *(reference_coordinates)
    acceleration = acceleration_controller[0]
    robot_angular_velocity = acceleration_controller[1]
    robot_linear_velocity = robot_velocity + acceleration*dt

    velocity_msg = Twist()
    velocity_msg.linear.x = float(robot_linear_velocity)
    velocity_msg.linear.y = float(robot_angular_velocity)
    publisher.publish(velocity_msg)
    

def main():
    global node, publisher , desired_pose , robot_velocity,time_a,bot_angle

    rclpy.init()
    node = Node('kinematics')
    node.create_subscription( Pose, '/turtle1/pose', get_turtlesim_pose, 10)
    publisher = node.create_publisher(Twist, '/turtle1/cmd_vel', 10)
    node.create_timer(0.5, send_turtlesim_cmd_vel)
    robot_velocity=1
    time_a=time.time()
    bot_angle=0
    rclpy.spin(node)

    
    

if __name__ == '__main__':
    main()  