class Gripper:

    def __init__(self, id1):
        self.id = id1
        self.setup_completed = 0

        # Process varibles
        self.claw_counter = 0  # this counter saves the current condition of the claw (how far is it opened) goes from 0 (open) to 30 (closed)
        self.start_closing = False
        self.closed = 0
        self.open = 0
        self.start_condition = False

        self.x_position = 0  # Arm is backwards (initial x) Range 0 - 175
        self.y_position = 160  # Gripper arm is at top (initial y) Range 0-160
        self.z_position = 0  # Rotated all the way to taster (initial z) Range 0-270

        self.x_destination = 0
        self.y_destination = 160  # Max range 0 - 160 (bottom til top)
        self.z_destination = 0

        # These are the coordinates to indicate where the gripper should pick something up and to what destination to bring it
        self.start_x = 0
        self.start_y = 160
        self.start_z = 0

        self.end_x = 0
        self.end_y = 160
        self.end_z = 0

        self.x_reached = False
        self.y_reached = False
        self.z_reached = False

        self.picked_up = False
        self.dropped_off = False
        self.at_base = False

        # Inputs (first 4 are for the encoder)
        self.vert_enc_1 = False
        self.vert_enc_2 = False
        self.rot_enc_1 = False
        self.rot_enc_2 = False
        self.taster_arm_in = False
        self.taster_arm_movement = 0
        self.taster_claw_open = False
        self.taster_claw_movement = 0
        self.taster_top = False
        self.taster_rot = False

        # Outputs
        self.arm_forward = False
        self.arm_backwards = False
        self.arm_up = False
        self.arm_down = False
        self.claw_open = False
        self.claw_close = False
        self.rotate_clockwise = False
        self.rotate_anticlockwise = False

    def setup(self):
        """This function brings the machine in the right starting position.
        The arm will be all the way back at the top and will be rotated to the origin"""

        # Step 1: arm goes fully in
        if not self.taster_arm_in:
            self.arm_backwards = True
        else:
            self.arm_backwards = False
            self.x_reached = True

        # Step 2: Arm is at the top
        if self.x_reached:
            if not self.taster_top:
                self.arm_up = True
            else:
                self.arm_up = False
                self.y_reached = True

        # Step 3: Rotate arm to origin
        if self.y_reached:
            if not self.taster_rot:
                self.rotate_clockwise = True
            else:
                self.rotate_clockwise = False
                self.z_reached = True

        # Open claw all the way (to drop whatever might be stuck) and close claw
        if not self.closed and self.y_reached:
            if not self.open:
                self.open_claw_fully()
            else:
                self.close_claw()

        if self.x_reached and self.y_reached and self.z_reached and self.closed:
            self.setup_completed = 1
            self.x_reached = False
            self.y_reached = False
            self.z_reached = False

    def open_claw_fully(self):
        if not self.open:
            if not self.taster_claw_open:
                self.claw_open = True
            else:
                self.claw_open = False
                self.closed = False
                self.open = True

    def set_start_and_end_destination(self, sx, sy, sz, ex, ey, ez):  # TODO Check if values are in range
        self.start_x = sx
        self.start_y = sy
        self.start_z = sz

        self.end_x = ex
        self.end_y = ey
        self.end_z = ez

    def going_to_x_destination(self):
        if not self.x_reached:
            if self.x_position < self.x_destination:
                self.arm_forward = True
                self.x_position += 1
                self.arm_backwards = False
                self.x_reached = False
            if self.x_position > self.x_destination:
                self.arm_forward = False
                self.arm_backwards = True
                self.x_position -= 1
                self.x_reached = False
            if self.x_position == self.x_destination:
                self.arm_forward = False
                self.arm_backwards = False
                self.x_reached = True
                print("arrived to x destination")

    def going_to_y_destination(self):
        if not self.y_reached:
            if self.y_position < self.y_destination:
                self.y_reached = False
                self.arm_up = True
                self.arm_down = False
            if self.y_position > self.y_destination:
                self.y_reached = False
                self.arm_up = False
                self.arm_down = True
            if self.y_position == self.y_destination:
                self.arm_up = False
                self.arm_down = False
                self.y_reached = True
                print("arrived to y destination")
            self.count_y_movement()

    def count_y_movement(self):
        if (self.vert_enc_1 and self.vert_enc_2) or (not self.vert_enc_1 and not self.vert_enc_2) or (
                self.vert_enc_1 and not self.vert_enc_2) or (not self.vert_enc_1 and self.vert_enc_2):
            if self.arm_up:
                self.y_position += 1  # counts up each takt
            if self.arm_down:
                self.y_position -= 1  # counts down each takt

    def going_to_z_destination(self):
        if not self.z_reached:
            if self.z_position < self.z_destination:
                self.z_reached = False
                self.rotate_anticlockwise = True
                self.rotate_clockwise = False
            if self.z_position > self.z_destination:
                self.z_reached = False
                self.rotate_anticlockwise = False
                self.rotate_clockwise = True
            if self.z_position == self.z_destination:
                self.rotate_anticlockwise = False
                self.rotate_clockwise = False
                self.z_reached = True
                print("arrived to z destination")
            self.count_z_movement()

    def count_z_movement(self):
        if (self.rot_enc_1 and self.rot_enc_2) or (not self.rot_enc_1 and not self.rot_enc_2) or (
                self.rot_enc_1 and not self.rot_enc_2) or (not self.rot_enc_1 and self.rot_enc_2):
            if self.rotate_anticlockwise:
                self.z_position += 1  # counts up each takt
            if self.rotate_clockwise:
                self.z_position -= 1  # counts down each takt

    def transport(self):
        """ In order to not destroy the components when transporting, before rotating, the gripper arm should always be completely in and at the top"""
        print("Prepping Transport")  # Make smarter with go to x y z destination, didnt work
        self.x_destination = 0
        self.y_destination = 160

        if not self.at_base:
            if not self.taster_top:
                self.arm_up = True
                self.arm_down = False
            if self.taster_top:
                self.y_reached = True
                self.arm_up = False
                self.arm_down = False
            if self.y_reached:
                if not self.taster_arm_in:
                    self.arm_backwards = True
                    self.arm_forward = False
                if self.taster_arm_in:
                    self.x_reached = True
                    self.arm_backwards = False
                    self.arm_forward = False
            if self.x_reached and self.dropped_off:
                if not self.taster_rot:
                    self.rotate_clockwise = True
                    self.rotate_anticlockwise = False
                else:
                    self.rotate_clockwise = False
                    self.rotate_anticlockwise = False
                    self.at_base = True
                    self.x_reached = False
                    self.y_reached = False
                    self.z_reached = False
                    self.x_position = 0
                    self.y_position = 160
                    self.z_position = 0
            if self.x_reached and not self.dropped_off:
                self.at_base = True
                self.x_reached = False
                self.y_reached = False
                self.z_reached = False
                self.x_position = 0
                self.y_position = 160

    def open_claw(self):
        # Open Claw
        if not self.open:
            if self.claw_counter > 20:
                self.claw_open = True
                self.claw_counter -= 1
            else:
                self.claw_open = False
                self.closed = False
                self.open = True

    def close_claw(self):
        if not self.closed:
            if self.claw_counter < 31:
                self.claw_close = True
                self.claw_counter += 1
            else:
                self.claw_close = False
                self.open = False
                self.closed = True

    def complete_process(self):
        """The arm first goes to the destination, opens the claw, moves until it has the product, closes the claw and goes back to safe position.
        This function is also used for dropping of product, as it also has to go to the drop off destination, open the claw"""
        if not self.picked_up and not self.dropped_off:
            self.x_destination = self.start_x
            self.y_destination = self.start_y
            self.z_destination = self.start_z

            self.going_to_z_destination()
            if self.z_reached:
                self.going_to_y_destination()
            if self.y_reached:
                self.open_claw()
                if self.open:
                    self.going_to_x_destination()
            if self.x_reached:
                self.close_claw()
                if self.closed:
                    self.picked_up = True
                    self.x_reached = False
                    self.y_reached = False
                    self.z_reached = False

        if self.picked_up and not self.at_base:
            self.transport()

        if self.picked_up and self.at_base and not self.dropped_off:
            self.x_destination = self.end_x
            self.y_destination = self.end_y
            self.z_destination = self.end_z

            self.going_to_z_destination()
            if self.z_reached:
                self.going_to_x_destination()
            if self.x_reached:
                self.going_to_y_destination()
            if self.y_reached:
                self.open_claw()
                if self.open:
                    self.picked_up = False
                    self.dropped_off = True
                    self.at_base = False
                    self.x_reached = False
                    self.y_reached = False
                    self.z_reached = False

        if self.dropped_off:
            self.transport()
            if self.at_base:
                self.close_claw()
                if self.closed:
                    self.x_reached = False
                    self.y_reached = False
                    self.z_reached = False
                    self.dropped_off = False
                    self.at_base = False
                    self.start_condition = False

    def run(self):

        if self.start_condition:
            self.complete_process()

    def cleanup(self):
        self.arm_forward = False
        self.arm_backwards = False
        self.arm_up = False
        self.arm_down = False
        self.claw_open = False
        self.claw_close = False
        self.rotate_clockwise = False
        self.rotate_anticlockwise = False
