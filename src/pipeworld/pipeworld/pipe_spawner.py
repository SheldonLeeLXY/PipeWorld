import rclpy
import sys
from rclpy.node import Node
from std_srvs.srv import Empty
from gazebo_msgs.srv import SpawnEntity
from random import seed, uniform
from math import cos, sin, tan, atan2, pi, sqrt, ceil

MODEL_TAG = '<?xml version="1.0"?>\n<sdf version="1.4">\n<model name="model_name">\n<pose> pos_x pos_y pos_z roll pitch yaw </pose>\n<static>true</static>'
LINK_TAG = '<link name="link_name">\n\t<pose> pos_x pos_y pos_z roll pitch yaw </pose>\nTAGS\n</link>'
COMP_TAG = '\t<type name="the_name">\n\t\t<pose> pos_x pos_y pos_z roll pitch yaw </pose>\n\t\t<geometry>\n\t\t\t<box>\n\t\t\t\t<size>size_x size_y size_z</size>\n\t\t\t</box>\n\t\t</geometry>\n\t</type>'
pose_variables = ['pos_x','pos_y','pos_z','roll','pitch','yaw']
size_variables = ['size_x', 'size_y', 'size_z']

class PipeSpawner(Node):

    def __init__(self, panels, pipe_width):
        super().__init__('pipe_spawner')
        self.panels = panels
        self.thickness = 0.02
        self.radius = pipe_width/2 + self.thickness/2
        self.height = pipe_width/2 + 0.001
        self.spawn_entity = self.create_client(SpawnEntity, '/spawn_entity')
        while not self.spawn_entity.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('spawn entity service not available, waiting again...')
        self.unpause = self.create_client(Empty, '/unpause_physics')
        while not self.spawn_entity.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('unpause service not available, waiting again...')

    def spawn_network(self, points):
        for i in range(len(points)-1):
            a,b = points[i], points[(i+1)%len(points)]
            x_diff,y_diff = b[0]-a[0], b[1]-a[1]
            length = sqrt(x_diff**2 + y_diff**2)
            angle = atan2(y_diff,x_diff)
            #pipe is not full length to leave space for joints on both ends
            self.spawn_pipe('pipe_'+str(i), length - 2*self.radius, [a[0] + cos(angle)*length/2, a[1] + sin(angle)*length/2, self.height, 0, 0, angle])
            if(i<len(points)-2):
                c = points[(i+2)%len(points)]
                angle2 = atan2(c[1]-b[1], c[0]-b[0])
                angle_diff = atan2(a[1] - b[1], a[0] - b[0]) - atan2(c[1] - b[1], c[0] - b[0])
                smallest_angle_diff = atan2(sin(angle_diff), cos(angle_diff))
                self.spawn_joint('joint_'+str(i), smallest_angle_diff, [b[0],b[1],self.height,0,0,angle])
            

    def cylinder_link(self,length,name,half=False):
        link = LINK_TAG.replace('link_name',name)
        angle_increment = 2*pi/self.panels
        size = [length, self.thickness, 2*sin(angle_increment/2)*(self.radius+self.thickness)]
        comp_tag = COMP_TAG
        for size_val,size_var in zip(size,size_variables):
                comp_tag = comp_tag.replace(size_var,str(size_val))

        angle = 0
        panels = self.panels
        if(half):
            start=ceil(panels/2)
        for i in range(panels):
            visual = comp_tag.replace('type','visual').replace('the_name','visual_'+str(i))
            collision = comp_tag.replace('type','collision').replace('the_name','collision_'+str(i))
            roll = pi/2 - angle
            pose = [0, cos(roll)*self.radius, sin(roll)*self.radius, roll, 0, 0]
            for pose_val,pose_var in zip(pose,pose_variables):
                visual = visual.replace(pose_var,str(pose_val))
                collision = collision.replace(pose_var,str(pose_val))
            angle += angle_increment
            link = link.replace('TAGS', visual + '\n' + collision + '\nTAGS')
        link = link.replace('TAGS','')
        return link
        
    def spawn_pipe(self, name, length, pose):
        model = MODEL_TAG.replace('model_name', name)
        link = self.cylinder_link(length,name)
        for pose_val,pose_var in zip([0,0,0,0,0,0],pose_variables):
            link = link.replace(pose_var,str(pose_val))
        model += link
        model += '</model></sdf>'
        self.spawn_model(model, name, pose)

    def spawn_joint(self, name, angle, pose):
        joint_radius = abs(tan(angle/2)*self.radius)
        joint_angle = pi-angle
        joint_angle = atan2(sin(joint_angle), cos(joint_angle))
        outer_radius = joint_radius + self.radius
        model = MODEL_TAG.replace('model_name', name)
        sign = 1
        if(angle<0):
            sign = -1
        angle_increment = sign*2*pi/self.panels
        sections = abs(round(self.panels * joint_angle/(2*pi)))+1
        section_length = 2*sin(angle_increment/2)*(outer_radius)
        yaw = 0
        for i in range(sections):
            section_pose = [sign*(sin(yaw)*joint_radius) - self.radius, -sign*(cos(yaw)*joint_radius - joint_radius), 0, 0, 0, yaw]
            link = self.cylinder_link(section_length,'section_'+str(i),True)
            for pose_val,pose_var in zip(section_pose,pose_variables):
                link = link.replace(pose_var,str(pose_val))
            model += link
            yaw += angle_increment
        model += '</model></sdf>'
        self.spawn_model(model, name, pose)

    def spawn_model(self, model, name, pose):
        for pose_val,pose_var in zip(pose,pose_variables):
            model = model.replace(pose_var,str(pose_val))
        spawn_req = SpawnEntity.Request()
        spawn_req.name = name
        spawn_req.xml = model
        future = self.spawn_entity.call_async(spawn_req)
        rclpy.spin_until_future_complete(self, future)
        future.result()

    def unpause_sim(self):
        future = self.unpause.call_async(Empty.Request())
        rclpy.spin_until_future_complete(self, future)
        return future.result()

def main(args=None):
    if args is None:
        args = sys.argv
    rclpy.init(args=args)
    diameter = 0.5
    if('-d' in args):
        diameter = float(args[args.index('-d') + 1])
    spawner = PipeSpawner(24,diameter)
    points = []
    points_str = ''
    if('--points' in args):
        points_str = args[args.index('--points') + 1]
        str_coord = points_str.split()
        for str_tuple in str_coord:
            x,y = str_tuple.strip('()').split(',')
            points.append((float(x),float(y)))
    else:
        points_str = '{(-1,0),(2,0),(3,3),(4,2),(4,1),(6,1)}'
        points = [(-1,0),(2,0),(3,3),(4,2),(4,1),(6,1)]
    spawner.get_logger().info('Generating and spawning pipes with following coordinates: '+points_str)
    
    spawner.spawn_network(points)
    spawner.get_logger().info('Pipes spawned.')
    if('--pause' not in args): 
        spawner.get_logger().info('Unpausing')
        spawner.unpause_sim()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
