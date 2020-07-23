import socket
from struct import pack, unpack
import numpy as np
import matplotlib.pyplot as plt
import rospy
import std_msgs.msg
from sensor_msgs.msg import PointField
from sensor_msgs import point_cloud2
from sensor_msgs.msg import PointCloud2
from std_msgs.msg import Header
from math import cos, sin
import time

def run():
    rospy.init_node("r2sonic_node")
    pub = rospy.Publisher("r2sonic_publisher", PointCloud2, queue_size=1)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((rospy.get_param('/ip_addr'), int(rospy.get_param('/port'))))

    fields = [PointField('x', 0, PointField.FLOAT32, 1),
             PointField('y', 4, PointField.FLOAT32, 1),
             PointField('z', 8, PointField.FLOAT32,1),
            PointField('angle', 12, PointField.FLOAT32, 1),
          PointField('range', 16, PointField.FLOAT32, 1),
          PointField('intensity', 20,  PointField.FLOAT32, 1),]

    while not rospy.is_shutdown():
        s1 = time.time()
        data, addr = sock.recvfrom(rospy.get_param('/message_size'))
        packetSize = unpack('!I', data[4:8])
        # Skip 8 - 12, 12 - 14
        sectionSize = unpack('!H', data[14:16]) 
        # Skip 16 - 52
        timeS, timeNS  = unpack('!II', data[40:48])
        pingNumber, pingPeriod, soundSpeed = unpack('!Iff', data[48:60])
        # Skip 60 - 64, 64 - 68, 68 - 72, 80 - 84, 84 - 88, 88 - 92, 92 - 96, 96 - 100, 100-104
        # Skip 104 - 106, 106 - 108, 108 - 112, 112 - 116, 116 - 120, 120 - 124
        # Skip 124 - 128, 128 - 132, 132 - 136, 136 - 140, 140 - 142
        nbPoints, sectionNameA, sectionNameB, sectionSize, scalingFactor = unpack('!HssHf', data[126:136])
        ranges = [0 for i in range(nbPoints)]
        for i in range(nbPoints):
            ranges[i] = unpack('!H', data[136+i*2:136+2+i*2])[0]*scalingFactor*soundSpeed/2
            
        # Skip [136 + 2 * nbPoints, 136 + 2 * 256 = 648]
        # Skip 648 - 650, 650 - 652
        angleFirst, angleLast = unpack('!ff', data[652:660])
        # Skip 660 - 664
        zOff, yOff, xOff = unpack('!fff', data[664:676])
        # Skip 676 - 680, 680 - 684, 684 - 686, 686 - 688
        scalingFactorI1 = unpack('!f', data[688:692])[0]
        intensities  = []
        for i in range(nbPoints):
            intensities.append( unpack('!H', data[692+i*2:692+i*2+2])[0])
        
        # Skip until 692 + 2 * 256 = 1204
        # Skip 1204 - 1206, 1206 - 1208
        depthGateMin, depthGateMax, depthGateSlope = unpack('!fff', data[1208:1220])
        
        ### ROS stuff
        ## Header
        h = Header(frame_id='r2sonic')
        h.stamp = rospy.Time.now()
        ## Data
        data = []
        angles = list(np.linspace(angleFirst, angleLast, nbPoints)) 
        for i in range(nbPoints):
            x = ranges[i]*cos(angles[i]) + xOff 
            y = ranges[i]*sin(angles[i]) + yOff 
            data.append([float(x),float(y), float(zOff), float(angles[i]), float(ranges[i]), float(intensities[i]*scalingFactorI1)])
        pointcloud = point_cloud2.create_cloud(h, fields, data)
        pointcloud.is_dense = True
        # pointcloud.is_bigendian = True
        #pcl::fromROSmsg(
        pub.publish(pointcloud)
        s2 = time.time()
        #rospy.Rate(10).sleep()
        
if __name__ == "__main__":
    run()
