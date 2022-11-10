import time

class MultiprocessingStation:

    def __init__(self, id1):
        self.id = id1
        self.setup_completed = 0

        # Process variables
        self.step = 1
        self.start_oven = 0
        self.end_oven = 0
        self.start_transport = 0
        self.oven_counter = 0
        self.vacuum_counter = 0
        self.drop_product = 0
        self.saw_done = 0
        self.saw_counter = 0
        self.end_condition = 0

        # Inputs
        self.vg_taster_right = 0
        self.vg_taster_left = 0
        self.table_at_vg = 0
        self.table_at_saw = 0
        self.table_at_cb = 0
        self.taster_oven_out = 0
        self.oven_lightbarrier = 0
        self.taster_oven_in = 0
        self.cb_lightbarrier = 0

        # Outputs
        self.door_open = 0
        self.vacuum = 0
        self.compressor = 0
        self.oven_motor_in = 0
        self.oven_motor_out = 0
        self.vg_motor_left = 0
        self.vg_motor_right = 0
        self.vg_down = 0
        self.saw_turning = 0
        self.table_clockwise = 0
        self.table_anticlockwise = 0
        self.oven_light = 0
        self.cb_fwd = 0
        self.push_off_table = 0

    def setup(self):
        """This function brings the machine in the right starting position"""
        # Conveyor not running
        self.cb_fwd = 0
        self.compressor = 1
        self.door_open = 1
        self.oven_light = 0
        self.push_off_table = 0
        self.saw_turning = 0
        self.vg_down = 0

        if not self.taster_oven_out:
            self.oven_motor_out = True
        else:
            self.oven_motor_out = False

        if not self.vg_taster_right:
            self.vg_motor_right = True
        else:
            self.vg_motor_right = False

        if not self.table_at_vg:
            self.table_anticlockwise = True
        else:
            self.table_anticlockwise = False

        if not self.oven_motor_out and not self.vg_motor_right and not self.table_anticlockwise:
            self.setup_completed = True

    def oven_processing(self):
        if not self.oven_lightbarrier:
            self.start_oven = 1

        if self.start_oven:
            self.compressor = True
            if not self.taster_oven_in:
                self.door_open = True
                self.oven_motor_in = True
            else:
                self.door_open = False
                self.oven_motor_in = False
                self.oven_light = True

                if self.oven_counter % 2 == 1:
                    self.oven_light = True
                else:
                    self.oven_light = False
                self.oven_counter += 1

                if self.oven_counter >= 31:
                    self.start_oven = False
                    self.oven_counter = 0
                    self.end_oven = True

        if self.end_oven:
            if not self.taster_oven_out:
                self.door_open = True
                self.oven_motor_out = True
            else:
                self.door_open = False
                self.oven_motor_out = False
                self.oven_light = False
                self.end_oven = 0
                self.step = 2

    def vg_transport(self):
        if not self.start_transport:
            if not self.vg_taster_left:
                self.vg_motor_left = True
            else:
                self.vg_motor_left = False
                self.vg_down = True
                self.vacuum_counter += 1
                if self.vacuum_counter == 20:
                    self.start_transport = True
                    self.vacuum_counter = 0

        if self.start_transport:
            if not self.vg_taster_right:
                self.vg_down = False
                self.vacuum = True
                self.vg_motor_right = True
            else:
                self.vg_motor_right = False
                self.drop_product = True

            if self.drop_product:
                self.vg_down = True
                self.vacuum_counter += 1
                if self.vacuum_counter == 10:
                    self.vacuum = False
                if self.vacuum_counter == 20:
                    self.vg_down = False
                    self.vacuum_counter = 0
                    self.start_transport = False
                    self.drop_product = False
                    self.step = 3

    def table_processing(self):
        if not self.saw_done:
            if not self.table_at_saw:
                self.table_clockwise = True
            else:
                self.table_clockwise = False
                self.saw_counter += 1
                self.saw_turning = True
                if self.saw_counter == 20:
                    self.saw_counter = 0
                    self.saw_turning = False
                    self.saw_done = True

        if self.saw_done:
            if not self.table_at_cb:
                self.table_clockwise = True
            else:
                self.table_clockwise = False
                self.push_off_table = True
                self.cb_fwd = True
                self.saw_done = False
                self.step = 4

    def table_to_vg(self):
        if not self.cb_lightbarrier:
            self.end_condition = True

        if self.end_condition:
            self.push_off_table = False
            self.compressor = False
            if not self.table_at_vg:
                self.push_off_table = False
                self.table_anticlockwise = True
            else:
                self.table_anticlockwise = False
                self.end_condition = False
                self.step = 5

    def cleanup(self):
        self.door_open = 0
        self.vacuum = 0
        self.compressor = 0
        self.oven_motor_in = 0
        self.oven_motor_out = 0
        self.vg_motor_left = 0
        self.vg_motor_right = 0
        self.vg_down = 0
        self.saw_turning = 0
        self.table_clockwise = 0
        self.table_anticlockwise = 0
        self.oven_light = 0
        self.cb_fwd = 0
        self.push_off_table = 0

    def run(self):
        if self.step == 1:
            self.oven_processing()
        if self.step == 2:
            self.vg_transport()
        if self.step == 3:
            self.table_processing()
        if self.step == 4:
            self.table_to_vg()
        if self.step == 5:
            self.cb_fwd = False
            self.step = 1


