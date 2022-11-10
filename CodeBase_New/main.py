import revpimodio2
from conveyor_belt import ConveyorBelt
from punching_maschine import PunchingMachine
from multiprocessing_station import MultiprocessingStation
from gripper import Gripper
from warehouse import Warehouse

class Productionline1:
    """Mainapp for RevPi"""

    def __init__(self):
        """Init MyRevPiApp class."""
        # Instantiate RevPiModIO
        self.rpi = revpimodio2.RevPiModIO(autorefresh=True)
        # Handle SIGINT / SIGTERM to exit program cleanly

        self.status_list = []

        # Create Objects
        self.cb1 = ConveyorBelt(1)
        self.cb2 = ConveyorBelt(2)
        self.cb3 = ConveyorBelt(3)
        self.pm = PunchingMachine(21)
        self.mps = MultiprocessingStation(1)
        self.gr1 = Gripper(1)
        self.gr2 = Gripper(2)
        self.wh1 = Warehouse(1)

        self.rpi.handlesignalend(self.cleanup_revpi)

    def cleanup_revpi(self):
        """Cleanup function to leave the RevPi in a defined state."""
        # Switch of LED and outputs before exit program

        self.rpi.core.a1green.value = False

        # when interrupted, turn all outputs to zero
        self.cb1.cleanup()
        self.cb2.cleanup()
        self.cb3.cleanup()
        self.pm.cleanup()
        self.mps.cleanup()
        self.gr1.cleanup()
        self.gr2.cleanup()
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
                self.pm.setup()
                self.cb1.setup()
                self.cb2.setup()
                self.cb3.setup()
                self.mps.setup()
                self.gr1.setup()
                self.gr2.setup()
                self.wh1.setup()

            else:
                self.cb1.run()
                self.cb2.run()
                self.cb3.run()
                self.pm.run()
                self.mps.run()
                self.gr1.run()
                self.gr2.run()
                self.wh1.run(1)

                if self.cb1.light_bottom and not self.gr2.start_condition and not self.cb2.wayback:
                    self.gr2.start_condition = True
                    self.gr2.set_start_and_end_destination(135, 85, 78, 50, 82, 10)

                if self.cb2.start_condition and self.cb2.wayback and not self.gr2.start_condition:
                    self.gr2.start_condition = True
                    self.gr2.set_start_and_end_destination(50, 82, 17, 30, 82, 150)

                if self.cb3.end_condition and not self.gr1.start_condition:  # change condition,connect with turtle bot
                    self.gr1.start_condition = True
                    self.gr1.set_start_and_end_destination(100, 40, 95, 135, 120, 20)

            self.write()

            # resets after using the machines in order for them to return to their original state
    def _get_setup_status(self):
        status = [self.pm.setup_completed,
                  self.cb1.setup_completed,
                  self.cb2.setup_completed,
                  self.cb3.setup_completed,
                  self.mps.setup_completed,
                  self.gr1.setup_completed,
                  self.gr2.setup_completed,
                  self.wh1.setup_completed]
        return status

    def read(self):
        """In this function the arguments are linked to the respective trigger/input"""
        # Read inputs of Punching Maschine and set them as the respective conditions
        self.pm.pm_cb.start_condition = (1-self.rpi.io.CB2_LIGHT_RIGHT.value)
        self.pm.pm_cb.end_condition = (1 - self.rpi.io.PM_LIGHT_RIGHT.value)
        self.pm.start_condition = (1 - self.rpi.io.PM_LIGHT_RIGHT.value)
        self.pm.PM_Taster_Top = self.rpi.io.PM_TASTER_TOP.value
        self.pm.PM_Taster_Bottom = self.rpi.io.PM_TASTER_BOTTOM.value

        # Read inputs of Conveyor Belt 1 and set them as the respective conditions
        self.cb1.start_condition = (1 - self.rpi.io.MPS_LIGHT_CB.value)
        self.cb1.end_condition = (1 - self.rpi.io.CB1_LIGHT_BOTTOM.value)

        # Read inputs of Conveyor Belt 2 and set them as the respective conditions
        self.cb2.start_condition = self.pm.pm_cb.wayback_reset = (1 - self.rpi.io.CB2_LIGHT_LEFT.value)
        self.cb2.end_condition = (1 - self.rpi.io.PM_LIGHT_LEFT.value)
        self.cb2.wayback_condition = (1 - self.rpi.io.PM_LIGHT_RIGHT.value)
        self.cb2.wayback_reset = (1 - self.rpi.io.CB3_LIGHT_RIGHT.value) #maybe change to something else

        # Read inputs of Conveyor Belt 3 and set them as the respective conditions
        self.cb3.start_condition = (1 - self.rpi.io.CB3_LIGHT_RIGHT.value)
        self.cb3.end_condition = (1 - self.rpi.io.CB3_LIGHT_LEFT.value)

        # Read inputs for the MPS
        self.mps.vg_taster_right = self.rpi.io.MPS_TASTER_VG_RIGHT_STOP.value
        self.mps.vg_taster_left = self.rpi.io.MPS_TASTER_VG_LEFT_STOP.value
        self.mps.table_at_vg = self.rpi.io.MPS_TASTER_TABLE_VG_STOP.value
        self.mps.table_at_saw = self.rpi.io.MPS_TASTER_TABLE_SAW_STOP.value
        self.mps.table_at_cb = self.rpi.io.MPS_TASTER_TABLE_CB_STOP.value
        self.mps.taster_oven_out = self.rpi.io.MPS_TASTER_OVEN_OUT_STOP.value
        self.mps.taster_oven_in = self.rpi.io.MPS_TASTER_OVEN_IN_STOP.value
        self.mps.oven_lightbarrier = self.rpi.io.MPS_LIGHT_OVEN.value
        self.mps.cb_lightbarrier = self.rpi.io.MPS_LIGHT_CB.value
        self.mps.stop_cb = (1 - self.rpi.io.CB1_LIGHT_BOTTOM.value)
        self.cb1.light_bottom = (1 - self.rpi.io.CB1_LIGHT_BOTTOM.value)

        # Inputs Gripper 1(first 4 are for the encoder)
        self.gr1.vert_enc_1 = self.rpi.io.GR1_VERT_ENC1.value
        self.gr1.vert_enc_2 = self.rpi.io.GR1_VERT_ENC2.value
        self.gr1.rot_enc_1 = self.rpi.io.GR1_ROT_ENC1.value
        self.gr1.rot_enc_2 = self.rpi.io.GR1_ROT_ENC2.value
        self.gr1.taster_arm_in = self.rpi.io.GR1_TASTER_ARM_STOP.value
        self.gr1.taster_arm_movement = self.rpi.io.GR1_TASTER_ARM_MOVEMENT.value
        self.gr1.taster_claw_open = self.rpi.io.GR1_TASTER_CLAW_MAX.value
        self.gr1.taster_claw_movement = self.rpi.io.GR1_TASTER_CLAW_MOVEMENT.value
        self.gr1.taster_top = self.rpi.io.GR1_TASTER_TOP.value
        self.gr1.taster_rot = self.rpi.io.GR1_TASTER_ROTATION.value

        # Inputs Gripper 2(first 4 are for the encoder)
        self.gr2.vert_enc_1 = self.rpi.io.GR2_VERT_ENC1.value
        self.gr2.vert_enc_2 = self.rpi.io.GR2_VERT_ENC2.value
        self.gr2.rot_enc_1 = self.rpi.io.GR2_ROT_ENC1.value
        self.gr2.rot_enc_2 = self.rpi.io.GR2_ROT_ENC2.value
        self.gr2.taster_arm_in = self.rpi.io.GR2_TASTER_ARM_STOP.value
        self.gr2.taster_arm_movement = self.rpi.io.GR2_TASTER_ARM_MOVEMENT.value
        self.gr2.taster_claw_open = self.rpi.io.GR2_TASTER_CLAW_MAX.value
        self.gr2.taster_claw_movement = self.rpi.io.GR2_TASTER_CLAW_MOVEMENT.value
        self.gr2.taster_top = self.rpi.io.GR2_TASTER_TOP.value
        self.gr2.taster_rot = self.rpi.io.GR2_TASTER_ROTATION.value

        # Inputs for Warehouse
        self.wh1.vert_enc_1 = self.rpi.io.WH_ENC_VERT_1.value
        self.wh1.vert_enc_2 = self.rpi.io.WH_ENC_VERT_2.value
        self.wh1.horz_enc_1 = self.rpi.io.WH_ENC_RL_1.value
        self.wh1.horz_enc_2 = self.rpi.io.WH_ENC_RL_2.value
        self.wh1.taster_right = self.rpi.io.WH_TASTER_RIGHT.value
        self.wh1.taster_arm_in = self.rpi.io.WH_TASTER_BACK.value
        self.wh1.taster_arm_out = self.rpi.io.WH_TASTER_FRONT.value
        self.wh1.taster_top = self.rpi.io.WH_TASTER_TOP.value
        self.wh1.wh_cb.end_condition = (1 - self.rpi.io.WH_LIGHT_BACK.value)
        self.wh1.wh_cb.start_condition = (1 - self.rpi.io.WH_LIGHT_FRONT.value)
        self.wh1.light_back = (1 - self.rpi.io.WH_LIGHT_BACK.value)

    def write(self):
        """This function writes the values from the functions to the Outputs of the RevPi"""
        # Write Outputs of Conveyor Belt 1
        self.rpi.io.CB1_MOTOR_FWD.value = self.cb1.conveyorActForward
        self.rpi.io.CB1_MOTOR_BWD.value = self.cb1.conveyorActBackward

        # Write Outputs of Conveyor Belt 2
        self.rpi.io.CB2_MOTOR_FWD.value = self.cb2.conveyorActForward
        self.rpi.io.CB2_MOTOR_BWD.value = self.cb2.conveyorActBackward

        # Write Outputs of Conveyor Belt 3
        self.rpi.io.CB3_MOTOR_FWD.value = self.cb3.conveyorActForward
        self.rpi.io.CB3_MOTOR_BWD.value = self.cb3.conveyorActBackward

        # Write Outputs of Punching Maschine
        self.rpi.io.PM_MOTOR_FWD.value = self.pm.pm_cb.conveyorActForward
        self.rpi.io.PM_MOTOR_BWD.value = self.pm.pm_cb.conveyorActBackward
        self.rpi.io.PM_PUNCHER_UP.value = self.pm.PM_Motor_Up
        self.rpi.io.PM_PUNCHER_DOWN.value = self.pm.PM_Motor_Down

        #Write outputs of MPS
        self.rpi.io.MPS_OVEN_DOOR.value = self.mps.door_open
        self.rpi.io.MPS_VG_VACUUM.value = self.mps.vacuum
        self.rpi.io.MPS_COMPRESSOR.value = self.mps.compressor
        self.rpi.io.MPS_OVEN_IN.value = self.mps.oven_motor_in
        self.rpi.io.MPS_OVEN_OUT.value = self.mps.oven_motor_out
        self.rpi.io.MPS_VG_LEFT.value = self.mps.vg_motor_left
        self.rpi.io.MPS_VG_RIGHT.value = self.mps.vg_motor_right
        self.rpi.io.MPS_VG_DOWN.value = self.mps.vg_down
        self.rpi.io.MPS_SAW.value = self.mps.saw_turning
        self.rpi.io.MPS_TABLE_CLOCKWISE.value = self.mps.table_clockwise
        self.rpi.io.MPS_TABLE_ANTICLOCKWISE.value = self.mps.table_anticlockwise
        self.rpi.io.MPS_OVEN_LIGHT.value = self.mps.oven_light
        self.rpi.io.MPS_MOTOR_CB_FWD.value = self.mps.cb_fwd
        self.rpi.io.MPS_TABLE_PUSH.value = self.mps.push_off_table

        # Write outputs of Gripper 1
        self.rpi.io.GR1_ARM_FWD.value = self.gr1.arm_forward
        self.rpi.io.GR1_ARM_BWD.value = self.gr1.arm_backwards
        self.rpi.io.GR1_ARM_UP.value = self.gr1.arm_up
        self.rpi.io.GR1_ARM_DOWN.value = self.gr1.arm_down
        self.rpi.io.GR1_CLAW_OPEN.value = self.gr1.claw_open
        self.rpi.io.GR1_CLAW_CLOSE.value = self.gr1.claw_close
        self.rpi.io.GR1_ARM_CLOCKWISE.value = self.gr1.rotate_clockwise
        self.rpi.io.GR1_ARM_ANTICLOCKWISE.value = self.gr1.rotate_anticlockwise

        #Write outputs of Gripper 2
        self.rpi.io.GR2_ARM_FWD.value = self.gr2.arm_forward
        self.rpi.io.GR2_ARM_BWD.value = self.gr2.arm_backwards
        self.rpi.io.GR2_ARM_UP.value = self.gr2.arm_up
        self.rpi.io.GR2_ARM_DOWN.value = self.gr2.arm_down
        self.rpi.io.GR2_CLAW_OPEN.value = self.gr2.claw_open
        self.rpi.io.GR2_CLAW_CLOSE.value = self.gr2.claw_close
        self.rpi.io.GR2_ARM_CLOCKWISE.value = self.gr2.rotate_clockwise
        self.rpi.io.GR2_ARM_ANTICLOCKWISE.value = self.gr2.rotate_anticlockwise

        #Write outputs of Warehouse
        self.rpi.io.WH_ARM_FWD.value = self.wh1.arm_forward
        self.rpi.io.WH_ARM_BWD.value = self.wh1.arm_backwards
        self.rpi.io.WH_ARM_UP.value = self.wh1.arm_up
        self.rpi.io.WH_ARM_DOWN.value = self.wh1.arm_down
        self.rpi.io.WH_CRANE_LEFT.value = self.wh1.crane_left
        self.rpi.io.WH_CRANE_RIGHT.value = self.wh1.crane_right
        self.rpi.io.WH_CB_IN.value = self.wh1.wh_cb.conveyorActForward
        self.rpi.io.WH_CB_OUT.value = self.wh1.wh_cb.conveyorActBackward


if __name__ == "__main__":
    # Start RevPiApp app
    root = Productionline1()
    root.start()
