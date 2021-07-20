import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped, PoseStamped

class NaviToPose(Node):
    def __init__(self):
        super().__init__('Navi_To_Pose')

        self.publisher_ini = self.create_publisher(PoseWithCovarianceStamped, 'initialpose', 10)
        self.publisher_goal = self.create_publisher(PoseStamped, 'goal_pose', 10)

        self.start_pose = PoseWithCovarianceStamped()
        #filling header with relevant information
        self.start_pose.header.frame_id = "map"
        self.start_pose.header.stamp = self.get_clock().now().to_msg()
        #filling payload with relevant information gathered from subscribing
        # to initialpose topic published by RVIZ via rostopic echo initialpose
        self.start_pose.pose.pose.position.x = -13.666181564331055
        self.start_pose.pose.pose.position.y = -0.01860250160098076
        self.start_pose.pose.pose.position.z = 0.0

        self.start_pose.pose.pose.orientation.x = 0.0
        self.start_pose.pose.pose.orientation.y = 0.0
        self.start_pose.pose.pose.orientation.z = -0.003591489689727315
        self.start_pose.pose.pose.orientation.w = 0.9999935505801067

        self.start_pose.pose.covariance[0] = 0.25
        self.start_pose.pose.covariance[7] = 0.25
        self.start_pose.pose.covariance[1:7] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0] 
        self.start_pose.pose.covariance[8:34] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] 
        self.start_pose.pose.covariance[35] = 0.06853891945200942

        self.get_logger().info('Publishing: "%s"' % self.start_pose)

        self.publisher_ini.publish(self.start_pose)


        time_period = 2
        self.timer = self.create_timer(time_period, self.timer_callback)


    def timer_callback(self):
        

        self.goal_pose = PoseStamped()
        self.start_pose.header.frame_id = "map"
        self.start_pose.header.stamp = self.get_clock().now().to_msg()

        self.goal_pose.pose.position.x = 1.0
        self.goal_pose.pose.position.y = 0.0
        self.goal_pose.pose.position.z = 0.0

        self.goal_pose.pose.orientation.x = 0.0
        self.goal_pose.pose.orientation.y = 0.0
        self.goal_pose.pose.orientation.z = 0.0
        self.goal_pose.pose.orientation.w = 1.0

        self.get_logger().info('Publishing: "%s"' % self.goal_pose)

        self.publisher_goal.publish(self.goal_pose)
        
        
def main():
    rclpy.init()
    node = NaviToPose()
    rclpy.spin(node)

if __name__ == '__main__':
    main()