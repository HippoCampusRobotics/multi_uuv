cmake_minimum_required(VERSION 3.0.2)
project(multi_uuv)

find_package(catkin REQUIRED COMPONENTS
  rospy
  roscpp
  message_generation
  std_msgs
  geometry_msgs
)

catkin_python_setup()

add_message_files(
  FILES
  PoseId.msg
  PoseIdStamped.msg
  PoseIdArray.msg
  AltControlDebug.msg
)

add_service_files(
  FILES
  SetValue.srv
)

generate_messages(
  DEPENDENCIES
  std_msgs
  geometry_msgs
)

catkin_package(CATKIN_DEPENDS
  message_runtime
  std_msgs
  geometry_msgs)

catkin_install_python(PROGRAMS
  nodes/attitude_mimic
  nodes/fake_vision
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
  

include_directories(${catkin_INCLUDE_DIRS})
