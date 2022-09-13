"""
Class for the punching machine. Saves the ID of the punching machine and also all the digital inputs and outputs in an 
ordered and readable fashion. Functions for the later usage of the class are used here.
"""
import time
# from statemachine import StateMachine, State


class PunchingMachine:

    def __init__(self, machine_id, photo_sensor_io: bool, photo_sensor_pm: bool, switch_up: bool,
                 switch_down: bool, motor_cv_fw: bool, motor_cv_bw: bool, motor_pm_up: bool, motor_pm_down):
        self.machine_id = machine_id
        self.photo_sensor_io = photo_sensor_io
        self.photo_sensor_pm = photo_sensor_pm
        self.switch_up = switch_up
        self.switch_down = switch_down
        self.motor_cv_fw = motor_cv_fw
        self.motor_cv_bw = motor_cv_bw
        self.motor_pm_up = motor_pm_up
        self.motor_pm_down = motor_pm_down
        self.switch_up_counter = 0  # variable used for the punching machine operation. Tracks the usage of the pm
        """
        idle = State("initial", initial=True)
        conveyor_fw = State("forward operation")
        conveyor_bw = State("backward operation")
        punching = State("punching")

        object_in_io_sensor = idle.to(conveyor_fw)
        conveyor_fw_to_pm = conveyor_fw.to(punching)
        pm_to_conveyor_bw = punching.to(conveyor_bw)
        finishing_up = conveyor_bw.to(idle)
        """
    def set_initial_state_pm(self):
        """
        For the initial state: If the punching machine is not in its highest position, it should move up
        until it has reached max. height. The rest of the actuators should remain inactive.
        """
        while self.switch_down is True:
            self.motor_pm_up = True
            if self.switch_up is True:
                self.motor_pm_up = False
        self.motor_cv_fw = False
        self.motor_cv_bw = False
        self.motor_pm_up = False
        self.motor_pm_down = False
        print("InitialState was executed")

    def conveyor_fw_operation(self):
        io_sensor_flag = 0
        if self.photo_sensor_io is False and io_sensor_flag is False:
            while self.photo_sensor_pm is True:
                io_sensor_flag = 1
                self.motor_cv_fw = True
                time.sleep(0.25)
            self.motor_cv_fw = False
        if self.photo_sensor_io is False and io_sensor_flag is True:
            self.motor_cv_fw = False
            print(f"2 Objects on the conveyor belt of {self.machine_id}.ERROR")
            time.sleep(1)
            # TODO: At a later stage implement a way of communicating this to the turtle bots via the PLC
        print("FW Operation was executed")

    def conveyor_bw_operation(self):
        if self.photo_sensor_pm is False and self.switch_up_counter % 2 == 0:
            while self.photo_sensor_io is True:
                self.motor_cv_bw = True
                time.sleep(0.25)
            self.motor_cv_bw = False
        print("BW Operation was executed")

    def punching_machine_operation(self):
        # if self.switch_up is True and self.photo_sensor_pm is False:
        """
        pm motor should only switch on if the upper switch has been pressed twice. Once on when it has reached max.
        height and once it has returned to its initial position.
        """
        if self.switch_up_counter % 2 == 0:
            self.switch_up_counter += 1
            while self.switch_down is False:
                self.motor_pm_down = True
            self.motor_pm_down = False
        while self.switch_up is False:
            self.motor_pm_up = True
            time.sleep(0.25)
        self.motor_pm_up = False
        self.switch_up_counter += 1
        print(f"Counter of how often the upper switch is being toggled: {self.switch_up_counter}.")
        print("PM was executed")
