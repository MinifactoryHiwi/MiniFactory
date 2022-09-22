"""
Class for controlling the operation of the conveyor belt. Saves the ID of the conveyor belt and also all the digital
inputs and outputs in an ordered and readable fashion. Functions for the later usage of the class are used here.
The basic conveyor belt should operation is based on the logical XOR condition. Depending on which sensor is giving out
a signal, the corresponding motor should start operating (until the other sensor is reached).
If both sensors are pressed or none is pressed the conveyor belt is either idle or should output an error.
"""
import time

# TODO: Add object counter, how many objects have passed the conveyor belt. Also mutual exclusion and some error cases


class ConveyorBelt:

    def __init__(self, conveyor_id, plc_object):
        self.conveyor_id = conveyor_id
        self.pulse_button = False
        self.in_sensor = False
        self.out_sensor = False
        self.motor_fw = False
        self.motor_bw = False
        self.plc_object = plc_object

    def out_sensor(self):
        return self.out_sensor

    def in_sensor(self):
        return self.in_sensor

    def pulse_button(self):
        return self.pulse_button

    @property
    def motor_fw(self):
        return self._motor_fw

    @motor_fw.setter
    def motor_fw(self, value):
        self._motor_fw = value

    @property
    def motor_bw(self):
        return self._motor_bw

    @motor_bw.setter
    def motor_bw(self, value):
        self._motor_bw = value

    def conveyor_operation_fw(self):
        print("Entered Conveyor FW Operation")
        if self.in_sensor is False and self.out_sensor is True:       # mutual exclusion
            print(f"No objects detected simultaneously")
            print("Entered forward if")
            while self.plc_object.digital_in5 is True:
                self.motor_fw = True
                self.plc_object.digital_out0 = self.motor_fw
            print("exited while-loop")
            time.sleep(0.75)
            self.motor_fw = False
            self.plc_object.digital_out0 = self.motor_fw

    def conveyor_operation_bw(self):
        print("Entered Conveyor BW Operation")
        if self.in_sensor is True and self.out_sensor is False:       # mutual exclusion
            print("Entered backward if")
            while self.plc_object.digital_in4 is True:
                self.motor_bw = True
                self.plc_object.digital_out1 = self.motor_bw
            print("Exited while-loop")
            time.sleep(0.75)
            self.motor_bw = False
            self.plc_object.digital_out1 = self.motor_bw

