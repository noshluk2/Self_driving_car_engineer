from time import sleep
import rclpy
from std_msgs.msg import String

rclpy.init()
node = rclpy.create_node('my_publisher')
pub = node.create_publisher(String, 'chatter', 10)
msg = String()
i = 0
while rclpy.ok():
    msg.data = f'Hello World: {i}'
    i += 1
    print(f'Publishing: "{msg.data}"')
    pub.publish(msg)
    sleep(0.5)