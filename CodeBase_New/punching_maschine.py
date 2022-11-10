from conveyor_belt import ConveyorBelt

class PunchingMachine:

    def __init__(self, id1):
        self.id = id1
        self.setup_completed = 0
        self.pm_cb = ConveyorBelt(21)

        self.start_condition = False
        self.end_condition = False

        # Inputs and Outputs
        self.PM_Taster_Top = False
        self.PM_Taster_Bottom = False
        self.PM_Motor_Up = False
        self.PM_Motor_Down = False

        self.wayback = 0
        self.puncher_counter = 0

    def setup(self):
        """This function brings the machine in the right starting position"""
        # Conveyor not running
        self.pm_cb.conveyorActBackward = False
        self.pm_cb.conveyorActForward = False

        # Puncher is at the top
        if not self.PM_Taster_Top:
            self.PM_Motor_Up = True
        else:
            self.setup_completed = 1
            self.PM_Motor_Up = False

    def punching(self):
        if self.start_condition: # Light barrier disrupted
            if self.puncher_counter == 0:
                if not self.PM_Taster_Bottom:
                    self.PM_Motor_Down = True
                else:
                    self.PM_Motor_Down = False
                    self.puncher_counter = 1
            if self.puncher_counter == 1:
                if not self.PM_Taster_Top:
                    self.PM_Motor_Up = True
                else:
                    self.PM_Motor_Up = False
                    self.pm_cb.wayback_condition = True

        if not self.start_condition: # when object leaves punching station
            self.puncher_counter = 0
            self.pm_cb.wayback_condition = False

    def run(self):
        self.pm_cb.run()
        self.punching()

    def cleanup(self):
        self.pm_cb.cleanup()
        self.PM_Motor_Up = False
        self.PM_Motor_Down = False
