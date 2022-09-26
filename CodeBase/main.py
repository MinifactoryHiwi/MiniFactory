from __future__ import print_function
from pixtendv2l import PiXtendV2L   # Import PiXtend V2 class
from punchingmachine import PunchingMachine
from conveyorbelt import ConveyorBelt
from sortingline import SortingLine

# PLC Object
p = PiXtendV2L()
# cb1 = ConveyorBelt(1, p)
# pm1 = PunchingMachine(1, p)
sl1 = SortingLine(1, p)

# Definitions of the Pins of the PLC (NOT FINAL)
"""
INPUTS:
DI0 = p.digital_in0  # Photo-transistor goods in/out punching machine
DI1 = p.digital_in1  # Photo-transistor punching machine
DI2 = p.digital_in2  # Switch punching machine up
DI3 = p.digital_in3  # Switch punching machine down

DI4 = p.digital_in4  # Conveyor Sensor in
DI5 = p.digital_in5  # Conveyor Sensor out
DI6 = p.digital_in6  # Conveyor Impulse Switch

DI7 = p.digital_in7  # Sorting Line Pulse Counter
DI8 = p.digital_in8  # Sorting Line light barrier in
DI9 = p.digital_in9  # Sorting Line light barrier after colour
DI10 = p.digital_in10 # Sorting Line light barrier white
DI11 = p.digital_in10 # Sorting Line light barrier red
DI12 = p.digital_in10 # Sorting Line light barrier blue

OUTPUTS:
DO0 = p.digital_out0  # Conveyor motor forward
DO1 = p.digital_out1  # Conveyor motor backward

D02 = p.digital_out2  # Motor conveyor forward punching machine
D03 = p.digital_out3  # Motor conveyor backward punching machine
D04 = p.digital_out4  # Motor punching machine up
D05 = p.digital_out5  # Motor punching machine down

D06 = p.digital_out6  # Motor conveyor sorting line
D07 = p.digital_out7  # Motor Compressor
D08 = p.digital_out8  # Valve White
D09 = p.digital_out9  # Valve Red
D010 = p.digital_out10  # Valve Blue

"""

# Variables to be used
inputs = []
outputs = []
cycle = 0


def update_input_pins():
    inputs.clear()
    inputs.append(p.digital_in0)
    inputs.append(p.digital_in1)
    inputs.append(p.digital_in2)
    inputs.append(p.digital_in3)
    inputs.append(p.digital_in4)
    inputs.append(p.digital_in5)
    inputs.append(p.digital_in6)
    inputs.append(p.digital_in7)
    inputs.append(p.digital_in8)
    inputs.append(p.digital_in9)
    inputs.append(p.digital_in10)
    inputs.append(p.digital_in11)
    inputs.append(p.digital_in12)
    inputs.append(p.digital_in13)
    print(f"Values of the inputs: {inputs} in update function TEST PURPOSE")
    return inputs


if p is not None:

    while True:

        try:

            # Check if SPI communication is running and the received data is correct
            if p.crc_header_in_error is False and p.crc_data_in_error is False:
                if cycle >= 1:

                    update_input_pins()

                    # pm1.photo_sensor_io = inputs[0]
                    # pm1.photo_sensor_pm = inputs[1]

                    # pm1.switch_up = inputs[2]
                    # pm1.switch_down = inputs[3]
                    # cb1.in_sensor = inputs[4]
                    # cb1.out_sensor = inputs[5]
                    # cb1.pulse_button = inputs[6]
                    sl1.light_barrier_in = inputs[9]
                    sl1.light_barrier_after_color = inputs[10]

                    # cb1.conveyor_operation_fw()

                    # pm1.set_initial_state_pm()
                    # pm1.conveyor_fw_operation()
                    # pm1.punching_machine_operation()
                    # pm1.conveyor_bw_operation()

                    # cb1.conveyor_operation_bw()

                    sl1.conveyor_op_to_light()
                    sl1.conveyor_op_light_to_end()

                cycle += 1
                print(cycle)

        except KeyboardInterrupt:
            p.close()
            del p
            p = None
            break
