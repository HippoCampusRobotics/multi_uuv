import rospy
import re
import hippocampus_common.node


def get_vehicle_number():
    """Extracts number from either the node's namespace or the explicitly
    set parameter.

    Probably only relevant in multi-uuv applications.

    Returns:
        int, None: Number of the vehicle or None if it could not
            successfully be identified.
    """
    vehicle_number = hippocampus_common.node.Node.get_param("~vehicle_number")
    if vehicle_number is not None:
        return vehicle_number
    name = rospy.get_namespace().replace("/", "")
    ids = re.findall(r"\d+", name)
    ids = [int(x) for x in ids]
    n_ids = len(ids)

    if n_ids < 1:
        rospy.logerr(
            "[%s] Could not identify my vehicle number from my namespace. "
            "Shutting down.", name)
        rospy.signal_shutdown("Could not identify ID")
        return None
    if n_ids > 1:
        rospy.logwarn(
            "There is more than one vehicle number identified from my namespace"
        )
    rospy.loginfo("Using vehicle number identified from namespace.")
    hippocampus_common.node.Node.set_param("~vehicle_number", ids[0])
    return ids[0]


def get_path_target_name(id):
    return "multi_uuv_path_target_{}".format(id)


def get_pose_name(id):
    return "multi_uuv_pose_{}".format(id)
