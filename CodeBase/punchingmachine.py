import time


class PunchingMachine:

    def __init__(self, punching_machine_id, plc_object):
        self.punching_machine_id = punching_machine_id
        self.plc_object = plc_object
        self.photo_sensor_io = False
        self.photo_sensor_pm = False
        self.switch_up = False
        self.switch_down = False
        self.motor_cv_fw = False
        self.motor_cv_bw = False
        self.motor_pm_up = False
        self.motor_pm_down = False

    def photo_sensor_io(self):
        return self.photo_sensor_io

    def photo_sensor_pm(self):
        return self.photo_sensor_pm

    def switch_up(self):
        return self.switch_up

    def switch_down(self):
        return self.switch_down

    @property
    def motor_pm_up(self):
        return self._motor_pm_up

    @motor_pm_up.setter
    def motor_pm_up(self, value):
        self._motor_pm_up = value

    @property
    def motor_pm_down(self):
        return self._motor_pm_up

    @motor_pm_down.setter
    def motor_pm_down(self, value):
        self._motor_pm_up = value

    @property
    def motor_cv_fw(self):
        return self._motor_cv_fw

    @motor_cv_fw.setter
    def motor_cv_fw(self, value):
        self._motor_cv_fw = value

    @property
    def motor_cv_bw(self):
        return self._motor_cv_bw

    @motor_cv_bw.setter
    def motor_cv_bw(self, value):
        self._motor_cv_bw = value

    def set_initial_state_pm(self):
        """
        For the initial state: If the punching machine is not in its highest position, it should move up
        until it has reached max. height. The rest of the actuators should remain inactive.
        """
        if self.switch_down is True:
            print("Set initial state")
            while self.plc_object.digital_in2 is False:
                time.sleep(0.5)
                self.motor_pm_up = True
                self.plc_object.digital_out4 = self.motor_pm_up
            self.motor_pm_up = False
            self.plc_object.digital_out4 = self.motor_pm_up
        if self.switch_up is True:
            print("Machine in its initial state")

    def conveyor_fw_operation(self):
        if self.photo_sensor_io is False and self.photo_sensor_pm is True:
            while self.plc_object.digital_in1 is True:
                self.motor_cv_fw = True
                self.plc_object.digital_out2 = self.motor_cv_fw
            self.motor_cv_fw = False
            self.plc_object.digital_out2 = self.motor_cv_fw
        print("Nothing to do in conveyor_fw_operation for pm")

    def conveyor_bw_operation(self):
        print("Entered conveyor_bw_operation of punching machine")
        if self.photo_sensor_io is True and self.photo_sensor_pm is False:
            while self.plc_object.digital_in0 is True:
                self.motor_cv_bw = True
                self.plc_object.digital_out3 = self.motor_cv_bw
            self.motor_cv_fw = False
            self.plc_object.digital_out3 = self.motor_cv_fw
        print("Nothing to do in conveyor_bw_operation for pm")

    def punching_machine_operation(self):
        """
        pm motor should only switch on if the upper switch has been pressed twice. Once on when it has reached max.
        height and once it has returned to its initial position.
        """
        if self.switch_up is True and self.photo_sensor_pm is False:
            while self.plc_object.digital_in3 is False:
                self.motor_pm_down = True
                self.plc_object.digital_out5 = self.motor_pm_down
            time.sleep(0.5)
            self.motor_pm_down = False
            self.plc_object.digital_out5 = self.motor_pm_down

            while self.plc_object.digital_in2 is False:
                self.motor_pm_up = True
                self.plc_object.digital_out4 = self.motor_pm_up
            time.sleep(0.5)
            self.motor_pm_up = False
            self.plc_object.digital_out4 = self.motor_pm_up

