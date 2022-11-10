from conveyor_belt import ConveyorBelt
class Warehouse:

    def __init__(self, id1):
        self.id = id1
        self.setup_completed = 0
        self.wh_cb = ConveyorBelt(31)
        self.start_condition = False  # starts putting in an object
        self.end_condition = False  # starts taking out an object

        # Process varibles
        self.x_position = 0
        self.y_position = 0

        self.x_destination = 0
        self.y_destination = 0
        self.coordinates = []

        self.current_sector = 0
        # These are the coordinates to indicate where the gripper should pick something up and to what destination to bring it
        self.start_x = 0
        self.start_y = 0

        self.end_x = 0
        self.end_y = 0

        self.step = 0
        self.is_in = False
        self.is_out = False
        self.y_reached = False
        self.x_reached = False
        self.picked_up = False
        self.at_base = False

        # Inputs (first 4 are for the encoder)
        self.vert_enc_1 = False
        self.vert_enc_2 = False
        self.horz_enc_1 = False
        self.horz_enc_2 = False
        self.taster_right = False
        self.taster_arm_in = False
        self.taster_arm_out = False
        self.taster_top = False
        self.light_back = False

        # Outputs
        self.arm_forward = False
        self.arm_backwards = False
        self.arm_up = False
        self.arm_down = False
        self.crane_left = False
        self.crane_right = False


    def setup(self):
        if not self.setup_completed:
            # dont move conveyor belt
            self.wh_cb.conveyorActBackward = False
            self.wh_cb.conveyorActForward = False

            # First: Arm in
            if not self.taster_arm_in:
                self.arm_backwards = True
            else:
                self.arm_backwards = False

            # Arm up
            if self.taster_arm_in and not self.taster_top:
                self.arm_up = True
            else:
                self.arm_up = False

            # Drive all the way to the right
            if self.taster_top and not self.taster_right and self.taster_arm_in:
                self.crane_right = True
            else:
                self.crane_right = False

            if not self.wh_cb.conveyorActBackward and not self.wh_cb.conveyorActForward and self.taster_right and self.taster_top and self.taster_arm_in:
                self.setup_completed = 1

    def get_coordinates(self, sector):  # TODO Fill with values for y and z
        if sector == 0:  # pick up position at the conveyor
            return [2, 60]
        if sector == 1:
            return [65, 0]
        if sector == 2:
            return [115, 0]
        if sector == 3:
            return [165, 0]
        if sector == 4:
            return [65, 28]
        if sector == 5:
            return [115, 28]
        if sector == 6:
            return [165, 28]
        if sector == 7:
            return [65, 56]
        if sector == 8:
            return [115, 56]
        if sector == 9:
            return [165, 56]

    def arm_going_in(self):
        if not self.is_in:
            if not self.taster_arm_in:
                self.arm_backwards = True
            else:
                self.arm_backwards = False
                self.is_in = True
                self.is_out = False

    def arm_going_out(self):
        if not self.is_out:
            if not self.taster_arm_out:
                self.arm_forward = True
            else:
                self.arm_forward = False
                self.is_out = True
                self.is_in = False

    def going_to_base(self):
        if not self.at_base:
            if not self.taster_arm_in:
                self.arm_backwards = True
            else:
                self.arm_backwards = False
                self.is_out = False
                if not self.taster_top:
                    self.arm_up = True
                else:
                    self.arm_up = False
                    self.y_position = 0
                    if not self.taster_right:
                        self.crane_right = True
                    else:
                        self.crane_right = False
                        self.x_position = 0
                        self.at_base = True

    def going_to_x_destination(self):  # move horizontally
        if not self.x_reached:

            if self.x_position < self.x_destination:
                self.crane_right = False
                self.crane_left = True
                self.x_reached = False

            if self.x_position == self.x_destination:
                self.crane_right = False
                self.crane_left = False
                self.x_reached = True
                print("arrived to x destination")
            self.count_x_movement()

    def going_to_y_destination(self):  # move arm up and down
        if not self.y_reached:

            if self.y_position > self.y_destination:
                self.y_reached = False
                self.arm_up = True
                self.arm_down = False
            if self.y_position < self.y_destination:
                self.y_reached = False
                self.arm_up = False
                self.arm_down = True
            if self.y_position == self.y_destination:
                self.arm_up = False
                self.arm_down = False
                self.y_reached = True
                print("arrived to y destination")
            self.count_y_movement()

    def count_x_movement(
            self):  # TODO Dont forget to implement for going the other direction (getting something from warehouse)
        if (self.vert_enc_1 and self.vert_enc_2) or (not self.vert_enc_1 and not self.vert_enc_2) or (
                self.vert_enc_1 and not self.vert_enc_2) or (not self.vert_enc_1 and self.vert_enc_2):
            self.x_position += 1  # counts up each takt

    def count_y_movement(self):
        if (self.horz_enc_1 and self.horz_enc_2) or (not self.horz_enc_1 and not self.horz_enc_2) or (
                self.horz_enc_1 and not self.horz_enc_2) or (not self.horz_enc_1 and self.horz_enc_2):
            if self.arm_up:
                self.y_position -= 1  # counts up each takt
            if self.arm_down:
                self.y_position += 1  # counts up each takt

    def move_to_destination(self):
        """First moves to x destination then to y destination"""
        if not self.y_reached:
            if not self.x_reached:
                self.going_to_x_destination()
            else:
                self.going_to_y_destination()

    def put_in(self):
        if not self.is_out:
            self.arm_going_out()
        else:
            if not self.y_reached:
                self.y_destination = self.coordinates[1] + 10
                self.going_to_y_destination()

    def pick_up(self):
        # go a little lower in order to go underneath
        if not self.picked_up:
            # go underneath the object
            if not self.y_reached and not self.is_out:
                self.y_destination = (self.coordinates[1] + 10)
                self.going_to_y_destination()

            # go all the way out
            if self.y_reached and not self.is_out:
                self.arm_going_out()
            else:
                self.y_reached = False

            # lift up the product
            if (self.y_position != (self.coordinates[1]-2)) and self.is_out:
                self.y_destination = (self.coordinates[1] - 2)
                self.going_to_y_destination()

            if (self.y_position == (self.coordinates[1]-2)) and self.is_out:
                self.picked_up = True

    def store_object(self, sector):
        """Object comes via the CB and gets stored in a designated sector of the warehouse"""
        # position at origin
        if self.start_condition:
            if self.step < 3:
                self.coordinates = self.get_coordinates(0)
                self.x_destination = self.coordinates[0]
                self.y_destination = self.coordinates[1]
            if self.step >= 3:
                self.coordinates = self.get_coordinates(sector)
                self.x_destination = self.coordinates[0]
                self.y_destination = self.coordinates[1]

            # go down to conveyor belt
            if self.step == 0:
                if not self.y_reached:
                    self.move_to_destination()
                else:
                    self.step = 1
                    self.y_reached = False

            # pick up the item
            if self.step == 1:
                if not self.picked_up:
                    self.pick_up()
                else:
                    self.step = 2
                    self.picked_up = False
                    self.is_out = False

            # go back to base
            if self.step == 2:
                if not self.at_base:
                    self.going_to_base()
                else:
                    self.y_reached = False
                    self.x_reached = False
                    self.at_base = False
                    self.is_out = False
                    self.step = 3

            # move to position
            if self.step == 3:
                if not self.y_reached:
                    self.move_to_destination()
                else:
                    self.step = 4
                    self.y_reached = False
                    self.x_reached = False

            # put it in the warehouse and go a little bit down to drop package
            if self.step == 4:
                if not self.y_reached:
                    self.put_in()
                else:
                    self.step = 5

            # move arm back in
            if self.step == 5:
                if not self.is_in:
                    self.arm_going_in()
                else:
                    self.step = 6

            # go back to initial position
            if self.step == 6:
                if not self.at_base:
                    self.going_to_base()
                else:
                    self.start_condition = False
                    self.y_reached = False
                    self.x_reached = False
                    self.at_base = False
                    self.step = 0

    def run(self, sector):
        self.wh_cb.run()
        if self.light_back:
            self.start_condition = True
        self.store_object(sector)

    def cleanup(self):
        self.wh_cb.cleanup()
        self.arm_forward = False
        self.arm_backwards = False
        self.arm_up = False
        self.arm_down = False
        self.crane_left = False
        self.crane_right = False

