# AUTONOMOUS DELIVERY ROBOT — ROS 2

## Summary of the Project

This project focuses on the development and simulation of an **Autonomous Indoor Delivery Robot** using **ROS 2 Jazzy, Gazebo Harmonic, SLAM Toolbox, Nav2, LiDAR, and RViz2**.

The goal of the project is to create a mobile robot capable of navigating autonomously inside structured indoor environments such as offices, hospitals, universities, warehouses, and research facilities.

The robot is simulated in a custom Gazebo office environment and uses a LiDAR sensor to perceive its surroundings. LiDAR measurements are published to ROS 2 as `LaserScan` data and are used by SLAM Toolbox to generate a two-dimensional occupancy map of the environment.

The robot uses differential-drive locomotion and publishes odometry information that is integrated into the ROS 2 TF coordinate system. After mapping the environment, the generated map can be saved and reused with the ROS 2 Navigation Stack (Nav2) for localization, path planning, obstacle avoidance, and autonomous goal-based navigation.

The project demonstrates the complete robotics pipeline:

**Simulation → Sensor Integration → Odometry → TF → SLAM → Mapping → Localization → Path Planning → Autonomous Navigation**

---

# Project Demo

## Gazebo Simulation

The following recording demonstrates the autonomous delivery robot operating inside the custom Gazebo office environment.

[▶ Watch Gazebo Robot Simulation](media/gazebo_office_demo.mp4)

## SLAM Mapping and RViz

The following recording demonstrates LiDAR-based mapping and visualization using SLAM Toolbox and RViz2.

[▶ Watch SLAM Mapping Demo](media/slam_nav2_demo.mp4)

---

# Key Features

- ROS 2 Jazzy based robotic system
- Custom autonomous delivery robot model
- Custom Gazebo office environment
- Differential-drive locomotion
- GPU LiDAR simulation
- ROS 2 ↔ Gazebo communication
- Real-time LaserScan data
- Robot odometry
- TF2 coordinate transformations
- SLAM Toolbox integration
- Real-time occupancy-grid mapping
- Map saving and loading
- RViz2 visualization
- Keyboard teleoperation
- Nav2 configuration
- AMCL localization support
- Global and local path planning
- Autonomous navigation architecture

---

# System Architecture

The overall system architecture is:

```text
                 CUSTOM GAZEBO OFFICE
                         |
                         v
                +------------------+
                |  Delivery Robot  |
                +------------------+
                    |           |
                    |           |
                  LiDAR      Diff Drive
                    |           |
                  /scan       /odom
                    |           |
                    +-----+-----+
                          |
                          v
                         TF2
                          |
                          v
                  +---------------+
                  | SLAM Toolbox  |
                  +---------------+
                          |
                         /map
                          |
                          v
                  +---------------+
                  |     AMCL      |
                  | Localization  |
                  +---------------+
                          |
                          v
                  +---------------+
                  |     Nav2      |
                  +---------------+
                    |           |
                Planner      Controller
                    \           /
                     \         /
                       /cmd_vel
                          |
                          v
                  +---------------+
                  | Delivery Robot|
                  +---------------+
```

---

# Software Requirements

The project was developed using:

| Technology | Purpose |
|---|---|
| Ubuntu | ROS development environment |
| WSL2 | Linux robotics development on Windows |
| ROS 2 Jazzy | Robotics middleware |
| Gazebo Harmonic | Robot simulation |
| RViz2 | Robot, sensor and map visualization |
| SLAM Toolbox | Simultaneous localization and mapping |
| Navigation2 | Autonomous navigation |
| AMCL | Robot localization |
| TF2 | Coordinate frame transformations |
| ros_gz_bridge | ROS 2 and Gazebo communication |
| URDF/Xacro | Robot description |
| SDF | Gazebo world description |
| CMake | ROS package build configuration |
| Git | Version control |
| GitHub | Project repository |

---

# Robot Model

The delivery robot is modeled using **URDF/Xacro**.

The robot contains:

- `base_footprint`
- `base_link`
- Left drive wheel
- Right drive wheel
- Caster wheel
- `lidar_link`
- GPU LiDAR sensor

The main robot description can be found at:

```text
ros2_ws/src/delivery_robot_description/urdf/delivery_robot.urdf.xacro
```

---

# Robot Coordinate Frames

The project uses ROS 2 TF2 to maintain the coordinate relationships between the map, robot, and sensors.

The primary TF hierarchy is:

```text
map
 |
 v
odom
 |
 v
base_footprint
 |
 v
base_link
 |
 v
lidar_link
 |
 v
LiDAR sensor frame
```

The `map -> odom` transform is generated during SLAM/localization.

The `odom -> base_footprint` transform represents the robot's motion.

The robot description provides the transforms between the robot body and sensor links.

---

# LiDAR Sensor

The robot uses a simulated GPU LiDAR sensor in Gazebo.

The LiDAR publishes laser measurements to:

```text
/scan
```

Message type:

```text
sensor_msgs/msg/LaserScan
```

LiDAR information is used by SLAM Toolbox to detect walls and obstacles and generate the occupancy map.

Example:

```bash
ros2 topic echo /scan
```

The LiDAR data can also be inspected using:

```bash
ros2 topic info /scan -v
```

---

# Differential Drive System

The robot uses differential-drive locomotion.

The two drive wheels allow the robot to:

- Move forward
- Move backward
- Rotate left
- Rotate right
- Stop

Velocity commands are received through:

```text
/cmd_vel
```

The robot publishes odometry through:

```text
/odom
```

---

# Important ROS 2 Topics

The primary ROS 2 topics used by the system include:

```text
/scan
/odom
/tf
/tf_static
/cmd_vel
/map
/map_metadata
/map_updates
/clock
/joint_states
/robot_description
```

---

# ROS 2 — Gazebo Bridge

`ros_gz_bridge` is used to exchange information between the Gazebo simulation and ROS 2.

The bridge allows ROS nodes to access simulated:

- LiDAR information
- Robot odometry
- Velocity commands
- TF information
- Simulation clock

This creates the communication pipeline:

```text
Gazebo
   |
   v
ros_gz_bridge
   |
   v
ROS 2
   |
   +------> SLAM
   |
   +------> RViz
   |
   +------> Nav2
```

---

# SLAM Mapping

The project uses **SLAM Toolbox** for mapping the simulated office environment.

SLAM Toolbox receives:

```text
/scan
/odom
/tf
```

and generates:

```text
/map
```

The robot is manually driven around the environment while the LiDAR scans surrounding walls and obstacles.

As the robot moves, SLAM Toolbox continuously updates the occupancy map.

The resulting map can be visualized in RViz2.

---

# Running SLAM Toolbox

After starting the robot simulation and ROS-Gazebo bridges:

```bash
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=true
```

In RViz2 set:

```text
Fixed Frame: map
```

Add:

```text
Map
LaserScan
TF
RobotModel
```

Set:

```text
Map Topic: /map
LaserScan Topic: /scan
```

---

# Driving the Robot

The robot can be manually controlled using `teleop_twist_keyboard`.

Run:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

Controls:

```text
   u    i    o
   j    k    l
   m    ,    .
```

Main controls:

```text
i  = Move Forward
,  = Move Backward

j  = Turn Left
l  = Turn Right

k  = Stop
```

Additional speed controls:

```text
q / z = Increase / decrease maximum speed
w / x = Increase / decrease linear speed
e / c = Increase / decrease angular speed
```

---

# Saving the Generated Map

After completing the mapping process, the generated occupancy map can be saved.

```bash
ros2 run nav2_map_server map_saver_cli \
-f src/delivery_robot_description/maps/delivery_office_map \
--ros-args \
-p use_sim_time:=true \
-p save_map_timeout:=10.0
```

This generates:

```text
delivery_office_map.pgm
delivery_office_map.yaml
```

---

# Saved Office Map

The generated map configuration is:

```yaml
image: delivery_office_map.pgm
mode: trinary
resolution: 0.050
origin: [-7.708, -10.850, 0]
negate: 0
occupied_thresh: 0.65
free_thresh: 0.196
```

The map resolution is:

```text
0.05 meters/pixel
```

The generated occupancy map is stored under:

```text
ros2_ws/src/delivery_robot_description/maps/
```

---

# Navigation2

After generating the map, **Nav2** can use the map for autonomous navigation.

Nav2 provides:

- Global path planning
- Local path planning
- Obstacle avoidance
- Costmap generation
- Goal execution
- Velocity command generation

The navigation pipeline is:

```text
Navigation Goal
      |
      v
Global Planner
      |
      v
Global Path
      |
      v
Local Controller
      |
      v
Obstacle Avoidance
      |
      v
/cmd_vel
      |
      v
Delivery Robot
```

---

# Localization

For navigation using a previously saved map, the robot can use **AMCL (Adaptive Monte Carlo Localization)**.

AMCL uses:

- Saved occupancy map
- LiDAR measurements
- Odometry
- TF transforms

to estimate the robot's position inside the map.

The localization pipeline is:

```text
Saved Map --------+
                  |
LiDAR /scan ------+----> AMCL ----> Robot Pose
                  |
Odometry ---------+
```

---

# Project Directory Structure

```text
autonomous_delivery_robot/
│
├── README.md
├── .gitignore
│
├── media/
│   ├── gazebo_office_demo.mp4
│   └── slam_nav2_demo.mp4
│
└── ros2_ws/
    │
    └── src/
        │
        └── delivery_robot_description/
            │
            ├── config/
            │   └── nav2_params.yaml
            │
            ├── launch/
            │   ├── display.launch.py
            │   └── gazebo.launch.py
            │
            ├── maps/
            │   ├── delivery_office_map.pgm
            │   └── delivery_office_map.yaml
            │
            ├── urdf/
            │   └── delivery_robot.urdf.xacro
            │
            ├── worlds/
            │   └── delivery_world.sdf
            │
            ├── CMakeLists.txt
            └── package.xml
```

---

# Building the Project

Clone the repository:

```bash
git clone <repository-url>
```

Enter the ROS 2 workspace:

```bash
cd autonomous-delivery-robot-ros2/ros2_ws
```

Source ROS 2 Jazzy:

```bash
source /opt/ros/jazzy/setup.bash
```

Install dependencies if required:

```bash
rosdep install --from-paths src --ignore-src -r -y
```

Build:

```bash
colcon build --symlink-install
```

Source the workspace:

```bash
source install/setup.bash
```

---

# Running the Simulation

After building the workspace:

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash
```

Launch the Gazebo simulation:

```bash
ros2 launch delivery_robot_description gazebo.launch.py
```

The custom office environment and delivery robot should appear in Gazebo.

---

# RViz Visualization

Launch RViz2:

```bash
rviz2 --ros-args -p use_sim_time:=true
```

Recommended displays:

```text
Grid
Map
LaserScan
TF
RobotModel
```

For SLAM:

```text
Fixed Frame = map
```

For robot/odometry debugging:

```text
Fixed Frame = odom
```

---

# Software Workflow

The autonomous delivery robot begins inside the simulated Gazebo office environment.

The differential-drive system provides robot movement while the LiDAR continuously scans the surrounding environment.

Gazebo sensor information is transferred into ROS 2 through `ros_gz_bridge`.

SLAM Toolbox combines the LiDAR measurements, odometry, and TF transformations to estimate robot motion and construct an occupancy map.

After the environment has been completely explored, the map is saved as `.pgm` and `.yaml` files.

The saved map can then be loaded into the Nav2 navigation system. AMCL estimates the robot's position within the known map while Nav2 calculates an appropriate path toward a user-defined navigation goal.

The controller converts the planned trajectory into `/cmd_vel` velocity commands, which are transmitted to the differential-drive robot.

This allows the robot to navigate through the simulated office environment autonomously.

---

# Current Project Status

| Module | Status |
|---|---|
| Robot URDF/Xacro | ✅ Completed |
| Differential Drive | ✅ Completed |
| Custom Gazebo Environment | ✅ Completed |
| LiDAR Integration | ✅ Completed |
| ROS-Gazebo Bridge | ✅ Completed |
| Odometry | ✅ Completed |
| TF Tree | ✅ Completed |
| Keyboard Teleoperation | ✅ Completed |
| SLAM Toolbox | ✅ Completed |
| Occupancy Map Generation | ✅ Completed |
| Map Saving | ✅ Completed |
| RViz Visualization | ✅ Completed |
| Nav2 Configuration | ✅ Implemented |
| AMCL Configuration | ✅ Implemented |
| Autonomous Navigation | 🚧 Continued testing/improvement |

---

# Challenges Solved

Several robotics integration challenges were addressed during development:

### LiDAR TF Integration

The Gazebo LiDAR sensor initially generated a sensor frame that was not directly connected to the robot TF tree.

The TF chain was corrected so that SLAM Toolbox could transform LiDAR measurements correctly.

### ROS 2 Simulation Time

SLAM, TF, RViz, and Gazebo were configured to use:

```text
use_sim_time:=true
```

This ensures that all components operate using the same Gazebo simulation clock.

### Map Frame

The `map` frame is generated by SLAM Toolbox after valid LiDAR, odometry, and TF information becomes available.

The resulting transform chain enables:

```text
map -> odom -> base_footprint -> base_link -> lidar
```

### Map Saving

The generated SLAM occupancy grid was successfully exported into reusable `.pgm` and `.yaml` map files for later autonomous navigation.

---

# Future Scope

The project can be expanded with:

1. **Computer Vision**

   Integrate an RGB/depth camera and YOLO for object and person detection.

2. **Dynamic Obstacle Avoidance**

   Improve navigation around moving people and other robots.

3. **Delivery Waypoints**

   Define named office locations such as:

   ```text
   Reception
   Office A
   Office B
   Meeting Room
   Delivery Station
   Charging Station
   ```

4. **Automatic Delivery Missions**

   Allow the robot to autonomously travel through multiple delivery locations.

5. **Battery Monitoring**

   Simulate battery consumption and automatically return the robot to a charging station.

6. **Automatic Docking**

   Implement autonomous charging-station docking.

7. **Multi-Robot Coordination**

   Extend the system to multiple delivery robots operating inside the same environment.

8. **Computer Vision + Robotics**

   Integrate object detection with autonomous navigation.

9. **LLM Robotics Copilot**

   Allow natural-language commands such as:

   ```text
   "Deliver this package to Office 3."
   ```

   to be converted into ROS 2 navigation tasks.

10. **Physical Robot Deployment**

    Transfer the simulation architecture to a real differential-drive mobile robot equipped with LiDAR, wheel encoders, and an onboard computer.

---

# Applications

This autonomous delivery architecture can be adapted for:

- Office document delivery
- Hospital medicine delivery
- Warehouse material transportation
- University campus delivery
- Laboratory logistics
- Hotel room service
- Manufacturing material handling
- Indoor service robotics

---

# Author

**Ganesh Paladugula**

Robotics | Artificial Intelligence | Autonomous Systems | Computer Vision

---

# Project Goal

The primary objective of this project is to demonstrate an end-to-end autonomous mobile robotics system combining:

**ROS 2 + Gazebo + LiDAR + TF2 + SLAM + Localization + Nav2**

to build a simulated autonomous delivery robot capable of mapping and navigating a structured indoor environment.
