import rclpy
from rclpy.node import Node

from cv_bridge import CvBridge
import numpy as np

from unitree_hg.msg import LowState, MotorState, LowCmd, MotorCmd
from unitree_go.msg import MotorStates, MotorCmds, SportModeCmd
from sensor_msgs.msg import Image
from std_msgs.msg import Bool
import json
import numpy as np
from decoupled_wbc.data.exporter import Gr00tDataExporter

class DataCollector(Node):
    def __init__(self):
        super().__init__('data_collector')
        self.bridge = CvBridge()
        self.motor_state_subscription = self.create_subscription(LowState, 'motor_states', self.motor_state_callback, 10)
        self.motor_cmd_subscription = self.create_subscription(LowCmd, 'motor_cmds', self.motor_cmd_callback, 10)
        self.camera_subscription = self.create_subscription(Image, 'camera/image_raw', self.camera_callback, 10)   
        self.lhand_state_subscription = self.create_subscription(MotorStates, 'lhand_states', self.lhand_state_callback, 10)
        self.rhand_state_subscription = self.create_subscription(MotorStates, 'rhand_states', self.rhand_state_callback, 10)
        self.lhand_cmd_subscription = self.create_subscription(MotorCmds, 'lhand_cmds', self.lhand_cmd_callback, 10)
        self.rhand_cmd_subscription = self.create_subscription(MotorCmds, 'rhand_cmds', self.rhand_cmd_callback, 10)

        self.control_subscription = self.create_subscription(Bool, '/control', self.control_subscription_callback, 10)

        self.velocity_subscription = self.create_subscription(SportModeCmd, '/velocity', self.base_velocity_callback, 10)

        self.latest_motor_state = None
        self.latest_motor_cmd = None
        self.latest_lhand_state = None
        self.latest_rhand_state = None
        self.latest_lhand_cmd = None
        self.latest_rhand_cmd = None
        self.MY_FEATURES = json.load(open("/home/deepak/Isaac-Gr00t-1.7/G1Inspire/features.json"))
        for feat in self.MY_FEATURES.values():
            feat["shape"] = tuple(feat["shape"])
        self.MY_MODALITY = json.load(open("/home/deepak/Isaac-Gr00t-1.7/G1Inspire/modality.json"))
        self.exporter = Gr00tDataExporter.create(
            save_root="/home/deepak/Isaac-Gr00t-1.7/G1Inspire/g1DataSet",
            fps=30,
            features=self.MY_FEATURES,
            modality_config=self.MY_MODALITY,
            task="wood-frame assembly",       # default task string for every frame
            overwrite_existing=True,        # wipe & recreate if the dir exists
        )   

        self.latest_base_velocity = None
        self.start_recording = False

    def base_velocity_callback(self, msg):
        self.latest_base_velocity = np.array([msg.velocity[0], msg.velocity[1], msg.yaw_speed, msg.body_height], dtype=np.float32);

    def lhand_state_callback(self, msg):
        self.latest_lhand_state = np.array([m.q for m in msg.states], dtype=np.float32);
    def rhand_state_callback(self, msg):
        self.latest_rhand_state = np.array([m.q for m in msg.states], dtype=np.float32);
    def lhand_cmd_callback(self, msg):
        self.latest_lhand_cmd = np.array([m.q for m in msg.cmds], dtype=np.float32);
    def rhand_cmd_callback(self, msg):
        self.latest_rhand_cmd = np.array([m.q for m in msg.cmds], dtype=np.float32);
    def motor_state_callback(self, msg):
        self.latest_motor_state = np.array([msg.motor_state[i].q for i in range(29)], dtype=np.float32);


    def motor_cmd_callback(self, msg):
        self.latest_motor_cmd = np.array([msg.motor_cmd[i].q for i in range(12,29)], dtype=np.float32);
    

    def camera_callback(self, msg):
        if (self.latest_motor_state is None or self.latest_motor_cmd is None or 
            self.latest_lhand_state is None or self.latest_rhand_state is None 
            or self.latest_lhand_cmd is None or self.latest_rhand_cmd is None
            or self.latest_base_velocity is None):
            return
        img = self.bridge.imgmsg_to_cv2(msg, desired_encoding="rgb8")  # (H, W, 3) numpy
        if (self.start_recording):
            latest_observation_state = np.concatenate((self.latest_motor_state, self.latest_lhand_state, self.latest_rhand_state), axis=0)
            latest_action = np.concatenate((self.latest_base_velocity,self.latest_motor_cmd, self.latest_lhand_cmd, self.latest_rhand_cmd), axis=0)
            self.exporter.add_frame({
                "observation.state":          latest_observation_state,
                "action":                     latest_action,
                "observation.images.ego_view": img     # (480,640,3) uint8 RGB
            })

    def control_subscription_callback(self, msg):
        
        if msg.data:
            self.start_recording = True
        else:
            if self.start_recording:
                self.exporter.save_episode()
                self.start_recording = False

        

if __name__ == '__main__':
    rclpy.init()
    data_collector = DataCollector() 
    rclpy.spin(data_collector)
    data_collector.destroy_node()
    rclpy.shutdown()
            
    


