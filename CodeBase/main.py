from __future__ import print_function
from pixtendv2l import PiXtendV2L   # Import PiXtend V2 class
# from punchingmachine import PunchingMachine
from conveyorbelt import ConveyorBelt
# import time

# PLC Object
p = PiXtendV2L()
cb1 = ConveyorBelt(1, p)

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
DI4 = p.digital_in4  # Sensor in
DI5 = p.digital_in5  # Sensor out
DI6 = p.digital_in6  # Impulse Switch
DO0 = p.digital_out0  # Conveyor motor forward
DO1 = p.digital_out1  # Conveyor motor backward
"""
# Variables to be used
inputs = []
outputs = []
cycle = 0


def update_input_pins():
    inputs.clear()
    inputs.append(p.digital_in4)
    inputs.append(p.digital_in5)
    inputs.append(p.digital_in6)
    print(f"Values of the inputs: {inputs} in update function TEST PURPOSE")
    return inputs


if p is not None:

    while True:

        try:

            # Check if SPI communication is running and the received data is correct
            if p.crc_header_in_error is False and p.crc_data_in_error is False:
                if cycle >= 1:
                    update_input_pins()
                    cb1.in_sensor = inputs[0]
                    cb1.out_sensor = inputs[1]
                    cb1.pulse_button = inputs[2]
                    cb1.conveyor_operation()

                cycle += 1
                print(cycle)

        except KeyboardInterrupt:
            p.close()
            del p
            p = None
            break
