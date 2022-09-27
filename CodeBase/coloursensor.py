import statistics as stat


class ColourSensor:

    def __init__(self, sensor_id, plc_object):
        self.sensor_id = sensor_id
        self.plc_object = plc_object
        # self.pin_input = 0
        self.recognized_color = 0.0
        self.init_values_color_sensor = []
        self.normalized_output = 0

    @property
    def recognized_color(self):
        return self._recognized_color

    @recognized_color.setter
    def recognized_color(self, value):
        self._recognized_color = value

    def object_detection(self):
        """
        This function runs in the background and evaluates the readings of the colour sensor. The specified pin is
        subject to change (p.analog_in0). The initial values of the continuous colour sensor reading are stored in an
        initial list. The list is made up of only a few elements, the mean of the initial elements builds the reference
        point. If significant changes to sensor values are being observed a separate list is used to store these
        changes. From this list we calculate the final output value of the colour detection plus a tolerance margin,
        which we then store and return in a dictionary.
        """
        detection_list = []
        delta_x = 0.3
        # i = 0
        # delta_y = 0.5
        lower_detection_bound = 0
        upper_detection_bound = 0
        reference_value = 0
        if self.plc_object.analog_in0 > 0.0 and len(self.init_values_color_sensor) <= 10:
            self.init_values_color_sensor.append(self.plc_object.analog_in0)
        print(self.init_values_color_sensor)
        if len(self.init_values_color_sensor) > 0:
            reference_value = stat.mean(self.init_values_color_sensor)
            print(f"reference value is: {reference_value}")

        if reference_value != 0:
            self.normalized_output = self.plc_object.analog_in0 / reference_value
            print(f"normalized output: {self.normalized_output}")
        if self.normalized_output != 1 and self.normalized_output > 0:
            if abs(self.plc_object.analog_in0 - reference_value) > delta_x:
                detection_list.append(self.plc_object.analogin0)
        print(detection_list)

        if len(detection_list) > 0:
            print(f"minimum value of list:{min(detection_list)}")
            print(f"maximum value of list:{max(detection_list)}")
            lower_detection_bound = min(detection_list)
            upper_detection_bound = max(detection_list)
            """
            upper_bound = min(detection_list) + delta_y
            lower_bound = min(detection_list) - delta_y
            while i < len(detection_list):
                if detection_list[i] > upper_bound or detection_list[i] < lower_bound:
                    detection_list.pop(i)
                i += 1
            """
        return lower_detection_bound, upper_detection_bound

    def color_recognition(self):
        detected_object = self.object_detection()
        if detected_object[0] is 0 and detected_object[1] is 0:
            print("No object passed the colour detection sensor")
            return 0
        else:
            if detected_object[0] > 5.5 and detected_object[1] < 6.1:
                print("Object Colour: Red")
                return 1
            if detected_object[0] > 6.5 and detected_object[1] < 7.2:
                print("Object Colour: Blue")
                return 2
            if detected_object[0] > 2 and detected_object[1] < 3:
                print("Object Colour:White")
                return 3


# Color recognition is hard coded right now: WILL BE CHANGED
# Object detection not yet optimal in its solution












