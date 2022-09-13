from __future__ import print_function
from pixtendv2l import PiXtendV2L   # Import PiXtend V2 class
# from punchingmachine import PunchingMachine
from conveyorbelt import ConveyorBelt
# import time

# PLC Object

p = PiXtendV2L()
# Definitions of the Pins of the PLC (NOT FINAL)
"""
I0 = p.digital_in0  # Photo-transistor goods in/out (conveyor belt)
I1 = p.digital_in1  # Photo-transistor punching machine
I2 = p.digital_in2  # Switch punching machine up
I3 = p.digital_in3  # Switch punching machine down
D4 = p.digital_out4  # Motor conveyor forward
D5 = p.digital_out5  # Motor conveyor backward
D6 = p.digital_out6  # Motor punching machine up
D7 = p.digital_out7  # Motor punching machine down
pm1 = PunchingMachine(1, I0, I1, I2, I3, D4, D5, D6, D7)
"""
I4 = p.digital_in4  # Sensor in
I5 = p.digital_in5  # Sensor out
I6 = p.digital_in6  # Impulse Switch
D0 = p.digital_out0  # Conveyor motor forward
D1 = p.digital_out1  # Conveyor motor backward
print(f"print {I4} and {I5} and {I6} and {D0} and {D1}")
cb1 = ConveyorBelt(1, I4, I5, I6, D0, D1)

"""
def read():
    inputs.clear()
    inputs.append(I4)
    inputs.append(I5)
    inputs.append(I6)


def write():
    outputs.clear()
    outputs.append(D0)
    outputs.append(D1)
"""

if p is not None:

    while True:

        try:
            # Check if SPI communication is running and the received data is correct
            if p.crc_header_in_error is False and p.crc_data_in_error is False:
                print(cb1.cb_inputs())
                print(cb1.cb_outputs())
                cb1.conveyor_operation()
                """
                pm1.set_initial_state_pm()
                time.sleep(2)
                print("initial state function called")
                if I0 is False:
                    pm1.conveyor_fw_operation()
                    time.sleep(2)
                    print("forward operation called")
                if I1 is False:
                    pm1.punching_machine_operation()
                    print("punching machine called")
                if I2 is True:
                    pm1.conveyor_bw_operation()
                    print("backward operation called")
                """
        except KeyboardInterrupt:
            p.close()
            del p
            p = None
            break
