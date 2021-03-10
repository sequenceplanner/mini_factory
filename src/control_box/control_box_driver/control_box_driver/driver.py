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
import RPi.GPIO as GPIO

from control_box_msgs.msg import Goal
from control_box_msgs.msg import Measured

from .spnode import SPNode

class ControlBoxDriver(SPNode):

    def __init__(self):
        super().__init__("control_box_driver")

        # initial goal (false)
        self.goal_to_json(Goal, Goal())

        self.GPO1 = 4
        self.GPO2 = 17
        self.GPO3 = 18
        self.GPO4 = 27
        self.GPI1 = 5
        self.GPI2 = 6
        self.GPI3 = 12
        self.GPI4 = 13
        self.GPI5 = 16
        self.GPI6 = 19
        self.GPI7 = 22
        self.GPI8 = 23

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.GPO1, GPIO.OUT, initial = False)
        GPIO.setup(self.GPO2, GPIO.OUT, initial = False)
        GPIO.setup(self.GPO3, GPIO.OUT, initial = False)
        GPIO.setup(self.GPO4, GPIO.OUT, initial = False)
        GPIO.setup(self.GPI1, GPIO.IN)
        GPIO.setup(self.GPI2, GPIO.IN)
        GPIO.setup(self.GPI3, GPIO.IN)
        GPIO.setup(self.GPI4, GPIO.IN)
        GPIO.setup(self.GPI5, GPIO.IN)
        GPIO.setup(self.GPI6, GPIO.IN)
        GPIO.setup(self.GPI7, GPIO.IN)
        GPIO.setup(self.GPI8, GPIO.IN)

        self.pub = self.create_publisher(Measured, "conveyor/measured")
        self.sub = self.create_subscription(Goal, "conveyor/goal", self.sub_callback)

        self.tmr = self.create_timer(0.01, self.timer_callback)

        self.measured = Measured()
        self.ticks = 0

        rclpy.spin(self)
        self.destroy_node()
        rclpy.shutdown()


    def timer_callback(self):
        new_measured = Measured()

        new_measured.sensor1 = GPIO.input(self.GPI1) == 1
        new_measured.sensor2 = GPIO.input(self.GPI2) == 1
        # new_measured.button = ...

        if self.measured != new_measured:
            self.measured = new_measured
            self.ticks = 0
            self.pub.publish(self.measured)

        self.ticks += 1
        if self.ticks > 100:
            self.ticks = 0
            self.pub.publish(self.measured)

    def sub_callback(self, data):
        GPIO.output(self.GPO1, data.run)
        GPIO.output(self.GPO2, data.direction)
        # GPIO.output(self.GPO3, data.out1)
        # GPIO.output(self.GPO4, data.out2)

        self.goal_to_json(Goal, data)

def main(args=None):
    rclpy.init(args=None)
    node = ControlBoxDriver()

if __name__ == '__main__':
    main()
