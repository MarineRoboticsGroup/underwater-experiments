import rospy
from sensor_msgs import point_cloud2
from sensor_msgs.msg import PointCloud2
from std_msgs.msg import Header

class PubSub():
    def __init__(self):
        self.pub = rospy.Publisher('centered_sonar', PointCloud2)
    
    def start(self):
        pass

    def callback(self, message):
        
        while not rospy.is_shutdown():
            try:
            (trans,rot) = listener.lookupTransform('odom', 'r2sonic', rospy.Time(0))
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                continue
        


