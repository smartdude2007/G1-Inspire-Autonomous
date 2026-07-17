install Groot wholebody controller

```
git clone https://github.com/NVlabs/GR00T-WholeBodyControl.git

python -m pip install -e "/home/deepak/Isaac-Gr00t-1.7/GR00T-WholeBodyControl/decoupled_wbc[full]"
```


Source unitree ros2
```
source unitree_ros2/cyclonedds_ws/src/unitree/install/setup.bash 
```

ssh into the humanoid and set up communication with the inspire hands

```
ssh unitree@192.168.123.164
cd dfx_inspire_service/build/
sudo ./inspire_g1
```

Run the teleoperation stack

collect data by running the data_collector script

```
cd Isaac-GR00T/examples/G1Inspire
python data_collector.py
```

publish to the control topics to control when to start and stop each episode

```
