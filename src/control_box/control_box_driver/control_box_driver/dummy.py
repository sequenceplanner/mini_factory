#!/usr/bin/env python

#----------------------------------------------------------------------------------------
# authors, description, version
#----------------------------------------------------------------------------------------
    # Endre Eres, Martin Dahl, Kristofer
    # PI driver
    # V.0.1.1.
#----------------------------------------------------------------------------------------

import sys
import time
import rclpy

from control_box_msgs.msg import Goal
from control_box_msgs.msg import Measured

from .spnode import SPNode

class ControlBoxDummy(SPNode):

    def __init__(self):
        super().__init__("control_box_dummy")
        self.goal_to_json(Goal, Goal())

        self.pub = self.create_publisher(Measured, "measured", 10)
        self.sub = self.create_subscription(Goal, "goal", self.sub_callback, 10)

        self.tmr = self.create_timer(0.01, self.timer_callback)

        self.measured = Measured()
        self.ticks = 0

        rclpy.spin(self)
        self.destroy_node()
        rclpy.shutdown()


    def timer_callback(self):
        self.ticks += 1
        if self.ticks > 100:
            self.ticks = 0
            self.pub.publish(self.measured)

    def sub_callback(self, data):
        self.goal_to_json(Goal, data)

def main(args=None):
    rclpy.init(args=None)
    node = ControlBoxDummy()

if __name__ == '__main__':
    main()
