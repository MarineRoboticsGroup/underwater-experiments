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

# Frames
* utm: Global UTM coordinate frame
* odom: Local fixed odometry frame
* odom2: odom translated to have its origin in the pool
* base_link: gantry frame
* r2sonic: sonar frame
* camera: optical center camera frame
