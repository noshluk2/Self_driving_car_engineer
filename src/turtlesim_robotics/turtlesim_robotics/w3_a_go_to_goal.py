"""
--> Go to Goal Node 
This is is a publisher(Command Velocity) and a subscriber(Pose) both 
- Takes in a goal specified in 2D
- Makes the robot calculate goal Heading
- Then Calculates Distance between the robot (through Pose) to Goal
- Send Command Velocities to reach the goal
- A tolerance is also set to make it easily converge

10/11/21
Author :
M.Luqman

"""
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt

def get_turtlesim_pose(data):
    global bot_pose
    bot_pose=data
    bot_pose.x=data.x
    bot_pose.y=data.y
    print(bot_pose.theta)
    

def send_turtlesim_cmd_vel():
    global bot_pose , pub , desired_pose
    distance_to_goal = sqrt(pow((desired_pose.x - bot_pose.x), 2) +  pow((desired_pose.y - bot_pose.y), 2))
    # test if we want to convert angle into degrees or not 
    angle_to_goal    = atan2(desired_pose.y - bot_pose.y, desired_pose.x - bot_pose.x)
    angle_to_turn    = angle_to_goal - bot_pose.theta
    new_vel= Twist()
    new_vel.linear.x = distance_to_goal
    new_vel.angular.z= angle_to_turn
    if (distance_to_goal>=0.5): # as it will never converge and overshoot
        pub.publish(new_vel)



def main(args=None):
    rclpy.init(args=args)

    global node, pub , desired_pose
    node = Node('Go_to_position_node')
    node.create_subscription(Pose,'/turtle1/pose',get_turtlesim_pose,10)
    desired_pose=Pose()
    desired_pose.x = 1.0
    desired_pose.y = 1.0
    pub=node.create_publisher(Twist,'/turtle1/cmd_vel',10)
    node.create_timer(0.5, send_turtlesim_cmd_vel)

    rclpy.spin(node)
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()