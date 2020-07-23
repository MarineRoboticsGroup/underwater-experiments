import rospy
from sensor_msgs import point_cloud2
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2 

class MySubscriber(object):
    def __init__(self):
        super().__init__()
        self.publisher = rospy.Publisher("edge_points", PointCloud2, queue_size=50)
        self.subs = rospy.Subscriber("r2sonic_publisher", PointCloud2, self.on_scan)

    def on_scan(self, scan):
        threshWIntensity = 0.003
        threshWOutIntensity = 0.01
        wIntensity = True

        cloud = list(pc2.read_points(scan, skip_nans=True, field_names=("x", "y", "z", "angle", "range", "intensity")))
        window_size = 5
        allScores = [0 for i in range(len(cloud))]
        nData = []
        for i in range(0, window_size):
            nData.append([cloud[i][0], cloud[i][1], cloud[i][2], cloud[i][3], cloud[i][4], 0])

        for ii in range(window_size, len(cloud) - window_size):
            score = - cloud[ii][4] * (2*window_size)
            for j in range(ii - window_size, ii + window_size):
                score += cloud[j][4]
            
            score = abs(score) / (cloud[ii][4] * 2 * window_size)

            d1 = cloud[ii-1][4] - cloud[ii][4]
            d2 = cloud[ii+1][4] - cloud[ii][4]
            # rospy.loginfo(cloud[ii])
            # rospy.loginfo(str(cloud[ii][0]**2+cloud[ii][1]**2))
            # rospy.loginfo(str(d1)+ " "+str(d2)+" " +str(d2- d1))
            if wIntensity:
                score = score * cloud[ii][5] / 1024

            if score < wIntensity*threshWIntensity+(1-wIntensity)*threshWOutIntensity or score > 0.1:
                score = 0
            else:
                if (abs(d2-d1) > 1e-7 and (abs(d1)/abs(d2-d1) > 5 and abs(d2)/abs(d2-d1) > 5)):
                    score = 0

            allScores[ii] = score 
            nData.append([cloud[ii][0], cloud[ii][1], cloud[ii][2], cloud[ii][3], cloud[ii][4], score])
            
        for i in range(len(cloud) - window_size, len(cloud)):
            nData.append([cloud[i][0], cloud[i][1], cloud[i][2], cloud[i][3], cloud[i][4], 0])

        nPointCloud = point_cloud2.create_cloud(scan.header, scan.fields, nData)
        self.publisher.publish(nPointCloud)


if __name__ == "__main__":
    rospy.init_node("smoothness_calculation")
    curSub = MySubscriber()
    rospy.spin()


