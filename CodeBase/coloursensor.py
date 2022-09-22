

class ColourSensor:

    def __init__(self, sensor_id, plc_object):
        self.sensor_id = sensor_id
        self.pin_input = 0
        self.plc_object = plc_object
        self.recognized_color = 0.0

    @property
    def recognized_color(self):
        return self._recognized_color

    @recognized_color.setter
    def recognized_color(self, value):
        self._recognized_color = value

    def color_recognition(self):
        pass





