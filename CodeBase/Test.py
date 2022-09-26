from __future__ import print_function
from pixtendv2l import PiXtendV2L
import csv
import time

p = PiXtendV2L()

"""
cycle = 0
inputs = []
outputs = []

def update_fct_inputs():

    inputs.clear()
    inputs.append(p.digital_in7)
    inputs.append(p.digital_in8)
    inputs.append(p.digital_in9)
    inputs.append(p.digital_in10)
    inputs.append(p.digital_in11)
    inputs.append(p.digital_in12)
    #print(f"Values of the inputs: {inputs} in update function")
    return inputs

def update_fct_outputs():
    p.digital_out0 = D0
    p.digital_out1 = D1
    outputs.clear()
    outputs.append(D0)
    outputs.append(D1)
    print(f"Values of the outputs: {outputs} in update function")
    return outputs

FILENAME = "AnalogSensor.csv"
header = ["Nr. of Steps", "SensorValues","ImpulseCounter"]
with open("AnalogSensor.csv", "w", encoding="UTF8") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerow(header)
"""
cycle_counter = 0
steps = 1
counter = 5
init_values = []     # first reading of analog sensor
default_sensor_value = 0
detection_red = []
normalized_sensor_output = 0
delta_x = 0.3
delta_y = 0.5

if p is not None:
    while True:
        try:

            if p.crc_header_in_error is False and p.crc_data_in_error is False and cycle_counter >= 1:
                """
                start_value_impulse_counter = p.digital_in7  # reading of the counter at the start of the program
                # print(f"Starting Value of Impulse Counter: {start_value_impulse_counter}")
                p.digital_out6 = True
                while p.digital_out6 is True and counter > 0:
                    print("entered while")
                    print(counter)
                    new_value_impulse_counter = p.digital_in7
                    print(f"New value impulse counter: {new_value_impulse_counter}")
                    if new_value_impulse_counter is not start_value_impulse_counter:
                        start_value_impulse_counter = new_value_impulse_counter
                        counter -= 1
                
                # print(f"init value:{init_values}")
                # print(f"value of sensor:{p.analog_in0}")
                if p.analog_in0 > 0.0 and steps <= 10:
                    init_values.append(p.analog_in0)
                    steps += 1
                    # print(f"{init_values} after {steps} steps")
                    if len(init_values) > 0 and sum(init_values) > 0:
                        default_sensor_value = sum(init_values)/len(init_values)
                print(f"Default_sensor_value {default_sensor_value}")
                p.digital_out6 = True
                if default_sensor_value != 0:
                    normalized_sensor_output = p.analog_in0 / default_sensor_value

                print(f"Normalized sensor output{normalized_sensor_output}")
                if normalized_sensor_output != 1 and normalized_sensor_output > 0:
                    if abs(p.analog_in0 - default_sensor_value) > delta_x:
                        detection_red.append(p.analog_in0)
                print(detection_red)

                if len(detection_red) > 0 and cycle_counter > 7000:
                    print(f"minimum value of red:{min(detection_red)}")
                    a = min(detection_red) + delta_y
                    b = min(detection_red) - delta_y
                    i = 0
                    while i < len(detection_red):
                        if detection_red[i] > a or detection_red[i] < b:
                            detection_red.pop(i)
                        i += 1
                # print(detection_red)
                """
                # p.digital_out7 = True
                # print(p.analog_in0)
                # print(f"Normalized Value {p.analog_in0/a}")
                # if p.analog_in0/a >= 0.5:
                #    print("Entered if")
                #    p.digital_out8 = False
                p.digital_out8 = True
                p.digital_out6 = True
                p.digital_out7 = True

                p.digital_out9 = True
                p.digital_out10 = True
                """
                a = p.analog_in0_raw
                f = open("AnalogSensor.csv", "a", newline="")
                writer = csv.writer(f, delimiter=",")
                writer.writerow([steps, a, start_value_impulse_counter])
                steps += 1
                f.close()
                """
            cycle_counter += 1
            print(cycle_counter)
            # print(f"{init_values} after {steps} steps")
        except KeyboardInterrupt:
            p.digital_out8 = False
            p.digital_out7 = False
            p.digital_out6 = False
            p.digital_out9 = False
            p.digital_out10 = False

            p.close()
            del p
            p = None
            break
