#!/usr/bin/env python

import pymavlink
import os
import time
from pymavlink.dialects.v20 import standard as mavlink

from pymavlink import mavutil

conn = mavutil.mavlink_connection("/dev/ttyUSB0",
                                  baud=57600,
                                  dialect="standard")

while True:
    time.sleep(0.1)
    conn.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_GCS,
                            mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)
    try:
        radio = conn.recv_match(type="RADIO_STATUS")
        if radio is not None:
            print(radio)
    except:
        print("Did not receive RADIO_STATUS")
