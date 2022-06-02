#!/usr/bin/env python

import rospy
from hippocampus_common.node import Node
from hippocampus_msgs.msg import PoseIdStamped
from mavros_msgs.msg import AttitudeTarget
from geometry_msgs.msg import Quaternion
import threading


class AttitudeMimicNode(Node):
    def __init__(self, name, anonymous=False, disable_signals=False):
        super().__init__(name,
                         anonymous=anonymous,
                         disable_signals=disable_signals)
        self.data_lock = threading.RLock()
        self.pubs = self.init_pubs()
        self.leader_id = self.get_param("~leader_id", 2)
        self.attitude_target = AttitudeTarget()
        self.attitude_target.orientation = Quaternion(x=0, y=0, z=0, w=0)
        self.subs = self.init_subs()

    def init_subs(self):
        subs = dict()
        subs["multi_uuv_pose"] = rospy.Subscriber("multi_uuv_pose",
                                                  PoseIdStamped,
                                                  self.on_multi_uuv_pose)
        return subs

    def init_pubs(self):
        pubs = dict()
        pubs["attitude_target"] = rospy.Publisher(
            "mavros/setpoint_raw/attitude", AttitudeTarget, queue_size=10)
        return pubs

    def on_multi_uuv_pose(self, msg: PoseIdStamped):
        id = msg.pose_id.id
        if id == self.leader_id:
            with self.data_lock:
                self.attitude_target.orientation = msg.pose_id.pose.orientation

    def run(self):
        r = rospy.Rate(30)
        while not rospy.is_shutdown():
            with self.data_lock:
                self.pubs["attitude_target"].publish(self.attitude_target)
            r.sleep()


def main():
    node = AttitudeMimicNode("attitude_mimic")
    node.run()


if __name__ == "__main__":
    main()
