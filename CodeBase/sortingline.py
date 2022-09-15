"""
Class for controlling the operation of the sorting line.
"""

import time


class SortingLine:

    def __init__(self, machine_id, light_barrier_in, light_barrier_after_color, color_sensor, light_barrier_red,
                 light_barrier_blue, light_barrier_white, conveyor_motor, compressor, valve_ejector_white,
                 valve_ejector_blue, valve_ejector_red):
        self.machine_id = machine_id
        self.light_barrier_in = light_barrier_in
        self.light_barrier_after_color = light_barrier_after_color
        self.color_sensor = color_sensor
        self.light_barrier_red = light_barrier_red
        self.light_barrier_blue = light_barrier_blue
        self.light_barrier_white = light_barrier_white
        self.conveyor_motor = conveyor_motor
        self.compressor = compressor
        self.valve_ejector_white = valve_ejector_white
        self.valve_ejector_blue = valve_ejector_blue
        self.valve_ejector_red = valve_ejector_red

    def set_initial_state(self):
        self.conveyor_motor = False
        self.compressor = False
        self.valve_ejector_red = False
        self.valve_ejector_white = False
        self.valve_ejector_blue = False

    def conveyor_operation(self):
        if self.light_barrier_in is False:
            self.conveyor_motor = True
            time.sleep(1)

    def analog_sensor(self):
        pass

    def colour_sorting(self):
        if self.light_barrier_after_color is False:
            pass

