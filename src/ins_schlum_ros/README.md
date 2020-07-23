ROS wrapper to read bathymetry data from the R2Sonic multibeam sonar 2020/2024 (https://www.r2sonic.com/products/sonic-2024/).
### Installation 
```
cd catkin_ws/src
git clone https://github.com/MarineRoboticsGroup/r2sonic_ros.git
catkin build
```

### Usage

`roslaunch r2sonic_ros r2sonic_test.launch`

### Remarks
The data from the sonar is read in *equi-angle* spacing mode (see documentation). 

The intensity is in micropascals, the angles in radians and the ranges in meters.
