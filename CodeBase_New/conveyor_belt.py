
class ConveyorBelt:

    def __init__(self, id1):
        self.id = id1
        self.setup_completed = 0

        self.start_condition = False
        self.end_condition = False

        self.conveyorActForward = self.conveyorActBackward = False

        self.wayback_condition = False

        self.wayback = False
        self. wayback_reset = False

    def setup(self):
        """This function brings the machine in the right starting position"""
        # Conveyor not running
        self.conveyorActForward = False
        self.conveyorActBackward = False
        self.setup_completed = 1

    def run(self):
        if not self.wayback: # driving conveyor belt forward
            if self.start_condition:
                print("Starting CB: " + str(self.id))
                self.conveyorActForward = True
            if self.end_condition:
                self.conveyorActForward = False

        if self.wayback_condition: # condition where the conveyor belt shoud change directions
            self.wayback = 1

        if self.wayback: # driving conveyor belt backwards
            if self.start_condition:
                self.conveyorActBackward = False
            if self.end_condition:
                self.conveyorActBackward = True
        if self.wayback_reset:
            self.wayback = 0

    def cleanup(self):
        self.conveyorActForward = False
        self.conveyorActBackward = False