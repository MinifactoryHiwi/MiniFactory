import revpimodio2
from warehouse import Warehouse


class EncoderTest:
    """Mainapp for RevPi"""

    def __init__(self):
        """Init MyRevPiApp class."""
        # Instantiate RevPiModIO
        self.rpi = revpimodio2.RevPiModIO(autorefresh=True)
        # Handle SIGINT / SIGTERM to exit program cleanly
        self.vg_go_up = False

        self.rpi.handlesignalend(self.cleanup_revpi)
        self.wh1 = Warehouse(1)

    def cleanup_revpi(self):
        """Cleanup function to leave the RevPi in a defined state."""
        # Switch of LED and outputs before exit program

        self.rpi.core.a1green.value = False
        self.wh1.cleanup()
        self.write()

    def start(self):
        """Start event system and own cyclic loop."""
        # Start event system without blocking here
        self.rpi.mainloop(blocking=False)
        print("Starting Mainloop")
        # My own loop to do some work next to the event system. We will stay
        # here till self.rpi.exitsignal.wait returns True after SIGINT/SIGTERM

        while not self.rpi.exitsignal.wait(0.05):
            # Value of the function rpi.exitsignal.wait can be changed. The argument of the function is the cycle time
            # of the plc.
            # Switch on / off green part of LED A1 | or do other things
            self.rpi.core.a1green.value = not self.rpi.core.a1green.value

            self.read()

            self.status_list = self._get_setup_status()

            if False in self.status_list:
                self.wh1.setup()
            else:
                self.wh1.run(3)

            self.write()

            # resets after using the machines in order for them to return to their original state

    def _get_setup_status(self):
        status = [self.wh1.setup_completed]
        return status

    def get_position_values(self):
        self.wh1.x_destination = 40
        self.wh1.going_to_x_destination()
        if self.wh1.x_reached:
            self.wh1.y_destination = 10
            if not self.wh1.y_reached:
                self.wh1.going_to_y_destination()

    def read(self):
        """In this function the arguments are linked to the respective trigger/input"""
        # Inputs Gripper 1(first 4 are for the encoder)
        # Inputs for Warehouse
        self.wh1.vert_enc_1 = self.rpi.io.I_8_i03.value
        self.wh1.vert_enc_2 = self.rpi.io.I_6_i03.value
        self.wh1.horz_enc_1 = self.rpi.io.I_7_i03.value
        self.wh1.horz_enc_2 = self.rpi.io.I_5_i03.value
        self.wh1.taster_right = self.rpi.io.WH_TASTER_RIGHT.value
        self.wh1.taster_arm_in = self.rpi.io.WH_TASTER_BACK.value
        self.wh1.taster_arm_out = self.rpi.io.WH_TASTER_FRONT.value
        self.wh1.taster_top = self.rpi.io.WH_TASTER_TOP.value
        #self.wh1.light_back = (1 - self.rpi.io.WH_LIGHT_BACK.value)

    def write(self):
        """This function writes the values from the functions to the Outputs of the RevPi"""
        #Write outputs of Warehouse
        self.rpi.io.WH_ARM_FWD.value = self.wh1.arm_forward
        self.rpi.io.WH_ARM_BWD.value = self.wh1.arm_backwards
        self.rpi.io.WH_ARM_UP.value = self.wh1.arm_up
        self.rpi.io.WH_ARM_DOWN.value = self.wh1.arm_down
        self.rpi.io.WH_CRANE_LEFT.value = self.wh1.crane_left
        self.rpi.io.WH_CRANE_RIGHT.value = self.wh1.crane_right
        #self.rpi.io.WH_CB_OUT.value = self.wh1.cb_out
        #self.rpi.io.WH_CB_IN.value = self.wh1.cb_in


if __name__ == "__main__":
    # Start RevPiApp app
    root = EncoderTest()
    root.start()
