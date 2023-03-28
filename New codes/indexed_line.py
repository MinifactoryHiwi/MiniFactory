from __future__ import print_function
import time
from pixtendv2l import PiXtendV2L  # Import PiXtend V2 class'''

p = PiXtendV2L()

while True:
    Q1 = p.digital_out1  # pin15
    Q2 = p.digital_out2  # pin16
    Q3 = p.digital_out3  # pin17
    Q4 = p.digital_out4  # pin18
    Q5 = p.digital_out5  # pin19
    Q6 = p.digital_out6  # pin20
    Q7 = p.digital_out7  # pin21
    Q8 = p.digital_out8  # pin22
    Q9 = p.digital_out9  # pin23
    Q10 = p.digital_out10  # pin24

    I1 = p.digital_in1  # pin5
    I2 = p.digital_in2  # pin6
    I3 = p.digital_in3  # pin7
    I4 = p.digital_in4  # pin8
    I5 = p.digital_in5  # pin9
    I6 = p.digital_in6  # pin10
    I7 = p.digital_in7  # pin11
    I8 = p.digital_in8  # pin12
    I9 = p.digital_in9  # pin13


    def conveyor_feed():
        I6 = p.digital_in6
        I8 = p.digital_in8
        print("workpiece fed to conveyor")
        print("value of I7", I7)
        print("value of I5", I5)
        print("value of I2", I2)
        print("value of I1", I1)
        print("value of I6", I6)
        p.digital_out5 = p.OFF
        if I7 is False:
            print("entered")
            p.digital_out5 = p.ON
            time.sleep(2)
            p.digital_out5 = p.OFF
            if I2 is True:
                p.digital_out1 = p.ON
                # time.sleep(2.7)
        if I1 is True:
            p.digital_out1 = p.OFF
            p.digital_out2 = p.ON
            time.sleep(2.5)
            p.digital_out2 = p.OFF
        # elif I2 is True:
        # p.digital_out2 = p.OFF
        # elif I1 is False and I2 is True:

        if I2 is False and I1 is True:
            p.digital_out7 = p.OFF
            while I6 is True:
                p.digital_out6 = p.ON
                p.digital_out7 = p.OFF
                I6 = p.digital_in6  # pin10
                if I6 is False:
                    p.digital_out6 = p.OFF
                    p.digital_out7 = p.ON
                    time.sleep(2)
                    p.digital_out6 = p.ON
                    p.digital_out6 = p.ON
                    p.digital_out6 = p.ON
                    p.digital_out6 = p.ON
            p.digital_out7 = p.OFF

            p.digital_out9 = p.OFF
            while I8 is True:
                p.digital_out8 = p.ON
                p.digital_out9 = p.OFF
                I8 = p.digital_in8  # pin10
                if I8 is False:
                    p.digital_out8 = p.OFF
                    p.digital_out9 = p.ON
                    time.sleep(2)
                    p.digital_out8 = p.ON
                    p.digital_out8 = p.ON
                    p.digital_out8 = p.ON
                    p.digital_out8 = p.ON
            p.digital_out9 = p.OFF
        if I8 is False and I4 is True:
            print("entered 2nd push")
            time.sleep(2)
            p.digital_out8 = p.OFF
            p.digital_out6 = p.OFF
            p.digital_out3 = p.ON
            # time.sleep(2.7)
        if I3 is True:
            p.digital_out3 = p.OFF
            p.digital_out4 = p.ON
            time.sleep(2.5)
            p.digital_out4 = p.OFF
            p.digital_out10 = p.ON
            if I9 is False:
                print("entered")
                time.sleep(1)
                p.digital_out10 = p.OFF







    '''if I9 is False:
        print("entered")
        time.sleep(2)
        p.digital_out10 = p.OFF'''

    conveyor_feed()

