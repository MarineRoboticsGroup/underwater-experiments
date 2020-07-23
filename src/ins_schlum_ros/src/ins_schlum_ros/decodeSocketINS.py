import socket
import math
from struct import pack, unpack
import numpy as np
import time
from nav_msgs.msg import Odometry
import rospy
from geometry_msgs.msg import PoseWithCovariance, Pose, Quaternion
import tf

def run():
    rospy.init_node("ins_schlum_ros", disable_rostime=True)
    pub = rospy.Publisher("nav_odom", Odometry, queue_size=50)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 19219))

    while True:
        data, addr = sock.recvfrom(61)
        # Skip 0
        seconds, mms = unpack('!IH', data[1:7])
        latitude, longitude, altitude, heave = unpack('!iiih', data[7:21])
        rospy.loginfo(altitude) 
        velNorth, velEast, velDown = unpack('!hhh', data[21:27])
        roll, pitch, heading = unpack('!hhH', data[27:33])
        roll = float(roll) * math.pi / 2**15.
        pitch = float(pitch) * math.pi / 2**15 
        heading = float(heading) * math.pi / 2**15 
        rotXV1, rotXV2, rotXV3 = unpack('!hhh', data[33:39])
        # Skip 39 - 43
        stdLat, stdLong, stdNVelo, stdEVelo, stdDVelo, stdRoll, stdPitch, stdHeading = unpack('!HHHHHHHH', data[43:59])
        checksum = unpack('!b', data[59:60])
        
        msg = Odometry()
        msg.child_frame_id = "base_link"        
        msg.pose.pose.position.y = float(latitude * 180.0 / 2**31)
        msg.pose.pose.position.x = float(longitude * 180.0 / 2**31)
        msg.pose.pose.position.z = float(altitude) / 100.0

        quaternion = tf.transformations.quaternion_from_euler(roll, -pitch, - heading)
        
        msg.pose.pose.orientation = Quaternion(*quaternion)
        # Let's discard it for now
        msg.pose.covariance = list(np.eye(6).flatten())
        msg.twist.twist.linear.x = velNorth / 100.0 # (m/s)
        msg.twist.twist.linear.y = velEast / 100.0 # (m/s)
        msg.twist.twist.linear.z = velDown /100.0 # (m/s)
        msg.twist.twist.angular.x = float(rotXV1) * math.pi /2**15
        msg.twist.twist.angular.y = float(rotXV3) * math.pi /2**15
        msg.twist.twist.angular.z = float(rotXV2) * math.pi /2**15
        pub.publish(msg)

if __name__ == "__main__":  
    run()
