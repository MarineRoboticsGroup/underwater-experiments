[![Build Status](http://mrg-beast.csail.mit.edu:8080/buildStatus/icon?job=underwater-experiments%2Fmaster)](http://mrg-beast.csail.mit.edu:8080/job/underwater-experiments/job/master/)

# Build instructions
```
git clone git@github.com:victor-amblard/underwater-experiments.git
cd underwater-experiments
catkin init
catkin_make
source devel/setup.bash
```
# Modules
* r2sonic_ros: Reads incoming data from the R2Sonic 2020 sonar and converts it in a `PointCloud2` format.
* ins_schlum_ros: Reads the data from the gantry system (lat/long/alt) and converts in an `Odometry` message 
* geonav_transform: geodesy transformations from LatLong to UTM, see https://github.com/bsb808/geonav_transform 
* ueye_camera: camera module, see  https://github.com/anqixu/ueye_cam

# Setup
The sonar is set to be connected at `10.23.0.41` on port `4000` in equi-angle mode.
Gantry messages are received on port `19219`.

# Frames
* utm: Global UTM coordinate frame 
* odom: Local fixed odometry frame (`utm-->odom` published by `geonav_transform`)
* odom2: odom translated to have its origin in the pool (cf. `experiment_sdr.launch` for `odom-->odom2`)
* base_link: gantry frame (`odom-->base_link` published by `geonav_transform`)
* r2sonic: sonar frame (cf `experiment_sdr.launch` for `base_link-->r2sonic`)
* camera: optical center camera frame (cf `experiment_sdr.launch` for `r2sonic-->camera`)

# Run!
```
roslaunch experiment_sdr.launch
```
RViz should automatically appear. Make sure to select `odom2` as the reference fixed frame.

To record a rosbag (note that only raw images are recorded).
```
rosbag record -a
```

