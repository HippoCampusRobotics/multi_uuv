import numpy


class PoseDict(dict):
    def __init__(self, pose_count=0):
        super(PoseDict, self).__init__()
        self.pose_count = pose_count

    def set_pose_count(self, n):
        self.pose_count = n

    def update_poses(self):
        pass


class PoseEntry(object):
    def __init__(self):
        self.position = numpy.array([0.0, 0.0])
        self.yaw = 0.0
        print("Hello from init")

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, position):
        self.__position = numpy.array(position).ravel()

    @property
    def yaw(self):
        return self.__yaw

    @yaw.setter
    def yaw(self, rad):
        if abs(rad) >= 2 * numpy.pi:
            rad = rad % (2 * numpy.pi)
        if rad < 0:
            rad += 2 * numpy.pi
        self.__yaw = rad
