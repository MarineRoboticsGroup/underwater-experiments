#!/usr/bin/env python

"""
Notes: Must be run with sudo due to raw socket connection
In order to keep environment variables while running python with sudo, try using
-E -P flags
If that fails, modify /etc/sudoers to include the following lines:

Defaults	env_keep += "PYTHONPATH"
Defaults	env_keep += "ROS_PACKAGE_PATH"


"""

import socket
import struct
import rospy
from geometry_msgs.msg import Point

def run(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((ip, port))

    # little endian format of pad byte, 3 signed long longs (8 byte integer), pad byte
    format = '<xqqqx'
    size = struct.calcsize(format)

    # setup ros connection
    pub = rospy.Publisher('gantry_pos', Point, queue_size=10)
    rospy.init_node("gantry", disable_rostime=True)
    r = rospy.Rate(10)
    print "started up"
    br = tf.TransformBroadcaster()
    # read from udp, publish as ros message
    while 1:
        msg, addr = s.recvfrom(1024) #TODO try with 26
        (x, y, z) = struct.unpack(format, msg)

        # spec conversions to inches
        #x /= 20792
        #y /= 20792
        #z /= 6931

        #print x, y, z

        ros_msg = Point(x, y, z)
        pub.publish(ros_msg)

        br.sendTransform((x,y,z), tf.transformations.quaternion_from_euler(0, 0, 0), rospy.Time.now(), "base_link", "odom")
        #r.sleep()


def main():
    # udp xyz packets are being sent to broadcast address on port 1000
    run("192.168.0.255", 1000)

if __name__ == '__main__':
    main()
