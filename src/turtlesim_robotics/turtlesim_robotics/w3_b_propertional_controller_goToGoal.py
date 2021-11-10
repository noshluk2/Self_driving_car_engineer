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
from std_msgs.msg import Float32
from turtlesim.msg import Pose
from math import pow, atan2, sqrt
import sys
class GTG(Node):
    def __init__(self):
        super().__init__('proportional_Controller_GTG')
        self.pose_subscriber              = self.create_subscription(Pose, '/turtle1/pose',self.get_turtlesim_pose,10)
        self.cmd_vel_publisher            = self.create_publisher(Twist,   '/turtle1/cmd_vel', 10)
        self.distance_error_publisher     = self.create_publisher(Float32, '/distance_error', 10)
        self.distance_set_point_publisher = self.create_publisher(Float32, '/distance_setpoint', 10)
        self.current_pos_value_publisher  = self.create_publisher(Float32, '/current_position', 10)
        timer_period = 0.5;self.timer  = self.create_timer(timer_period, self.send_turtlesim_cmd_vel)
        argv = sys.argv[1:]
  
        self.command_velocity=Twist()
        self.goal_pose=Pose();self.robot_pose=Pose();self.error_msg=Float32();
        self.set_point_msg=Float32();self.current_position=Float32()
        self.goal_pose.x = float(argv[0])
        self.goal_pose.y = float(argv[1])
        self.kp_distance=1
        self.kp_angle=6




    def get_turtlesim_pose(self,data):
        self.robot_pose.x=round(data.x,4)
        self.robot_pose.y=round(data.y,4)
        self.robot_pose.theta=data.theta

    def send_turtlesim_cmd_vel(self):
        distance_to_goal = sqrt(pow((self.goal_pose.x - self.robot_pose.x), 2) +  pow((self.goal_pose.y - self.robot_pose.y), 2))
        angle_to_goal    = atan2(self.goal_pose.y - self.robot_pose.y, self.goal_pose.x - self.robot_pose.x)
        angle_to_turn    = (angle_to_goal - self.robot_pose.theta)
        self.command_velocity.linear.x = self.kp_distance*distance_to_goal
        self.command_velocity.angular.z= self.kp_angle*angle_to_turn
        self.set_point_msg.data=self.goal_pose.x;
        self.error_msg.data=distance_to_goal;self.current_position.data=self.robot_pose.x
        if (distance_to_goal>=0.5): # as it will never converge and overshoot
            print("Distance to Goal ",round(distance_to_goal,4))
            print("Angle to Turn ",angle_to_turn)
            self.cmd_vel_publisher.publish(self.command_velocity)
        self.distance_set_point_publisher.publish(self.set_point_msg)
        self.distance_error_publisher.publish(self.error_msg)
        self.current_pos_value_publisher.publish(self.current_position)



def main(args=None):
    rclpy.init(args=args)
    turtlesim_controller=GTG()

    rclpy.spin(turtlesim_controller)
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()