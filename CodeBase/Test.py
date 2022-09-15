from __future__ import print_function
from pixtendv2l import PiXtendV2L
import time


p = PiXtendV2L()

cycle = 0
inputs = []
outputs = []


def update_fct_inputs():
    inputs.clear()
    inputs.append(p.digital_in4)
    inputs.append(p.digital_in5)
    inputs.append(p.digital_in6)
    print(f"Values of the inputs: {inputs} in update function")
    return inputs


# D0 = False
# D1 = False
# p.digital_out0 = D0
# p.digital_out1 = D1
"""
def update_fct_outputs():
    p.digital_out0 = D0
    p.digital_out1 = D1
    outputs.clear()
    outputs.append(D0)
    outputs.append(D1)
    print(f"Values of the outputs: {outputs} in update function")
    return outputs
"""

if p is not None:

    while True:

        try:
            """
            I4 = p.digital_in4  # Sensor in
            I5 = p.digital_in5  # Sensor out
            I6 = p.digital_in6  # Impulse Switch
            D0 = p.digital_out0  # Conveyor motor forward
            D1 = p.digital_out1  # Conveyor motor backward
            """
            # Check if SPI communication is running and the received data is correct
            if p.crc_header_in_error is False and p.crc_data_in_error is False:
                update_fct_inputs()
                # update_fct_outputs()
                print(f"Output of In-Sensor: {inputs[0]} and Out-Sensor: {inputs[1]} and Switch: {inputs[2]}")
                # print(f"Output of Motor-FW: {D0} and Motor-BW: {D1}")
                time.sleep(1)
                if inputs[0] is False and cycle >= 1:
                    while inputs[1] is True:
                        update_fct_inputs()
                        # update_fct_outputs()
                        # I5 = p.digital_in5
                        print("In-Sensor was false and Out-Sensor is true, we entered the if statement and while-loop")
                        # outputs[0] = p.ON
                        D0 = True
                        p.digital_out0 = D0
                        print(p.digital_out0)
                        if inputs[1] is False:
                            time.sleep(0.75)
                            # outputs[0] = False
                            D0 = False
                            p.digital_out0 = D0

                cycle += 1
                print(f"Number of cycles {cycle}")

        except KeyboardInterrupt:
            p.close()
            del p
            p = None
            break
