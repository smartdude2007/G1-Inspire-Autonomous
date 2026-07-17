import rclpy
from rclpy.node import Node
from unitree_hg.msg import LowState, MotorState, LowCmd, MotorCmd
import unitree_go.msg as go
from sensor_msgs.msg import Image
from std_msgs.msg import Bool
import numpy as np

class DataCollector(Node):
    def __init__(self):
        super().__init__('data_collector')
        self.motor_state_publisher = self.create_publisher(LowState, 'motor_states', 10)
        self.motor_cmd_publisher = self.create_publisher(LowCmd, 'motor_cmds', 10)
        self.camera_publisher = self.create_publisher(Image, 'camera/image_raw', 10)   
        self.lhand_state_publisher = self.create_publisher(go.MotorStates, 'lhand_states', 10)
        self.rhand_state_publisher = self.create_publisher(go.MotorStates, 'rhand_states', 10)
        self.lhand_cmd_publisher = self.create_publisher(go.MotorCmds, 'lhand_cmds', 10)
        self.rhand_cmd_publisher = self.create_publisher(go.MotorCmds, 'rhand_cmds', 10)

        self.velocity_publisher = self.create_publisher(go.SportModeCmd, '/velocity', 10);

        
        self.timer = self.create_timer(0.1, self.publish_data)  # Publish data every 0.1 seconds (10 Hz)

    
    def publish_data(self):
        self.publish_motor_state()
        self.publish_motor_cmd()
        self.publish_camera_image()
        self.publish_lhand_state()
        self.publish_rhand_state()
        self.publish_lhand_cmd()
        self.publish_rhand_cmd()
        self.publish_velocity()


    def publish_velocity(self):
        msg = go.SportModeCmd()
        msg.velocity = [0.0, 0.0]
        msg.yaw_speed = 0.0
        msg.body_height = 0.0
        self.velocity_publisher.publish(msg)
    
    def publish_motor_state(self):
        msg = LowState()
        for i in range(35):
            tmp = MotorState()
            tmp.q = 0.0  # Replace with actual motor state data;
            msg.motor_state[i] = tmp
        self.motor_state_publisher.publish(msg)

    def publish_motor_cmd(self):
        msg = LowCmd()
        for i in range(35):
            tmp = MotorCmd()
            tmp.q = 0.0  # Replace with actual motor command data;
            msg.motor_cmd[i] = tmp
        self.motor_cmd_publisher.publish(msg)
        
    def publish_camera_image(self):
        msg = self.create_dummy_image_msg()
        self.camera_publisher.publish(msg)

    def publish_lhand_state(self):
        msg = go.MotorStates()
        for i in range(6):
            tmp = go.MotorState()
            tmp.q = 0.0  # Replace with actual left hand state data;
            msg.states.append(tmp)
        self.lhand_state_publisher.publish(msg)

    def publish_rhand_state(self):
        msg = go.MotorStates()
        for i in range(6):
            tmp = go.MotorState()
            tmp.q = 0.0  # Replace with actual right hand state data;
            msg.states.append(tmp)
        self.rhand_state_publisher.publish(msg)

    def publish_lhand_cmd(self):
        msg = go.MotorCmds()
        for i in range(6):
            tmp = go.MotorCmd()
            tmp.q = 0.0  # Replace with actual left hand command data;
            msg.cmds.append(tmp)
        self.lhand_cmd_publisher.publish(msg)
    
    def publish_rhand_cmd(self):
        msg = go.MotorCmds()
        for i in range(6):
            tmp = go.MotorCmd()
            tmp.q = 0.0  # Replace with actual right hand command data;
            msg.cmds.append(tmp)
        self.rhand_cmd_publisher.publish(msg)

    def create_dummy_image_msg(self, width=1280, height=720, encoding='rgb8'):
        """
        Creates a dummy sensor_msgs/Image message filled with random pixel data.
        """
        msg = Image()

        # Header
        msg.height = height
        msg.width = width
        msg.encoding = encoding
        msg.is_bigendian = 0

        # Bytes per pixel based on encoding
        channels = {
            'rgb8': 3,
            'bgr8': 3,
            'rgba8': 4,
            'mono8': 1,
        }.get(encoding, 3)

        msg.step = width * channels

        # Generate random dummy image data
        dummy_data = np.random.randint(0, 255, (height, width, channels), dtype=np.uint8)
        msg.data = dummy_data.tobytes()

        return msg

if __name__ == '__main__':
    rclpy.init()
    data_collector = DataCollector()
    rclpy.spin(data_collector)
    data_collector.destroy_node()
    rclpy.shutdown()