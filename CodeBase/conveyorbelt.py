"""
Class for controlling the operation of the conveyor belt. Saves the ID of the punching machine and also all the digital
inputs and outputs in an ordered and readable fashion. Functions for the later usage of the class are used here.
"""
import time


class ConveyorBelt:

    def __init__(self, conveyor_id, pulse_button, in_sensor, out_sensor, motor_fw, motor_bw):
        self.conveyor_id = conveyor_id
        self.pulse_button = pulse_button
        self.in_sensor = in_sensor
        self.out_sensor = out_sensor
        self.motor_fw = motor_fw
        self.motor_bw = motor_bw

    def set_initial_state_cb(self):
        self.motor_fw = False
        self.motor_bw = False

    """
    Conveyor Belt should operate based on the logical XOR condition. Depending on which sensor is giving out a
    signal, the corresponding motor should start operating (until the other sensor is reached). 
    If both sensors are pressed or none is pressed the conveyor belt is either idle or should output an error.
    """

    def conveyor_fw(self):
        if self.in_sensor is True and self.out_sensor is False:
            while self.out_sensor is False:
                self.motor_fw = True
                time.sleep(0.25)
        self.motor_fw = False

    def conveyor_bw(self):
        if self.in_sensor is False and self.out_sensor is True:
            while self.in_sensor is False:
                self.motor_bw = True
                time.sleep(0.25)
        self.motor_bw = False

