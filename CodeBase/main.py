from __future__ import print_function
from pixtendv2l import PiXtendV2L   # Import PiXtend V2 class
from punchingmachine import PunchingMachine
# from conveyorbelt import ConveyorBelt

# PLC Object

p = PiXtendV2L()
# Definitions of the Pins of the PLC (NOT FINAL)
I0 = p.digital_in0  # Photo-transistor goods in/out (conveyor belt)
I1 = p.digital_in1  # Photo-transistor punching machine
I2 = p.digital_in2  # Switch punching machine up
I3 = p.digital_in3  # Switch punching machine down
D4 = p.digital_out4  # Motor conveyor forward
D5 = p.digital_out5  # Motor conveyor backward
D6 = p.digital_out6  # Motor punching machine up
D7 = p.digital_out7  # Motor punching machine down

if p is not None:

    while True:

        try:
            # Check if SPI communication is running and the received data is correct
            if p.crc_header_in_error is False and p.crc_data_in_error is False:
                pm1 = PunchingMachine(1, I0, I1, I2, I3, D4, D5, D6, D7)
                # cb1 = ConveyorBelt()
                pm1.set_initial_state_pm()
                pm1.conveyor_fw_operation()
                pm1.punching_machine_operation()
                pm1.conveyor_bw_operation()

        except KeyboardInterrupt:
            p.close()
            del p
            p = None
            break
