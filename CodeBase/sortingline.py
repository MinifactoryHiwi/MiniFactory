"""
Class for controlling the operation of the sorting line.
"""

import time
# from coloursensor import ColourSensor


class SortingLine:

    def __init__(self, machine_id, plc_object):
        self.machine_id = machine_id
        self.light_barrier_in = False
        self.light_barrier_after_color = False
        self.color_sensor = False
        self.light_barrier_red = False
        self.light_barrier_blue = False
        self.light_barrier_white = False
        self.conveyor_motor = False
        self.compressor = False
        self.valve_ejector_white = False
        self.valve_ejector_blue = False
        self.valve_ejector_red = False
        self.plc_object = plc_object
        self.impulse_counter = 5

# Basic Getters for the Inputs
    def light_barrier_in(self):
        return self.light_barrier_in

    def light_barrier_after_color(self):
        return self.light_barrier_after_color

    def color_sensor(self):
        return self.color_sensor

    def light_barrier_red(self):
        return self.light_barrier_red

    def light_barrier_blue(self):
        return self.light_barrier_blue

    def light_barrier_white(self):
        return self.light_barrier_white

# Encapsulated getters and setters for the outputs
    @property
    def conveyor_motor(self):
        return self._conveyor_motor

    @conveyor_motor.setter
    def conveyor_motor(self, value):
        self._conveyor_motor = value

    @property
    def compressor(self):
        return self._compressor

    @compressor.setter
    def compressor(self, value):
        self._compressor = value

    @property
    def valve_ejector_white(self):
        return self._valve_ejector_white

    @valve_ejector_white.setter
    def valve_ejector_white(self, value):
        self._valve_ejector_white = value

    @property
    def valve_ejector_red(self):
        return self._valve_ejector_white

    @valve_ejector_red.setter
    def valve_ejector_red(self, value):
        self._valve_ejector_red = value

    @property
    def valve_ejector_blue(self):
        return self._valve_ejector_blue

    @valve_ejector_blue.setter
    def valve_ejector_blue(self, value):
        self._valve_ejector_blue = value

# Functions for the operation of the sorting line

    def set_initial_state(self):
        pass

    def conveyor_op_to_light(self):
        print("ENTERED")
        print(f"light barrier in: {self.light_barrier_in}")
        if self.light_barrier_in is False and self.light_barrier_after_color is True:
            print(f"light barrier color is: {self.plc_object.digital_in10}")
            while self.plc_object.digital_in10 is True:
                print(f"Entered while loop. Value of motor before setting {self.plc_object.digital_out7}")
                self.conveyor_motor = True
                self.plc_object.digital_out7 = self.conveyor_motor
                print(f"Entered while loop. Value of motor after setting {self.plc_object.digital_out7}")
            self.conveyor_motor = False
            self.plc_object.digital_out7 = self.conveyor_motor
        print("Do nothing")

    def colour_sorting(self):
        if self.light_barrier_after_color is False:
            pass

    def conveyor_op_light_to_end(self):
        print("Entered")
        if self.light_barrier_in is False:
            print("light barrier detects object")
            self.compressor = True
            self.plc_object.digital_out8 = self.compressor
        if color_sensor_fct = 1:
            pass
        if color_sensor_fct = 2:
            pass:
        if color_sensor_fct = 3:
            pass:
        if color_sensor_fct =4:
            print("Let the object pass through")

