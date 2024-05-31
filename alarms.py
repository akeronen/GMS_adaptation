
class Object_alarms():
    def __init__(self):
        # supporting fifteen alarms
        self.alarms_list = [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ]

    def alarm_set(self, alarm_num, value):
        self.alarms_list[alarm_num] = value

    def alarm_get(self, alarm_num):
        return self.alarms_list[alarm_num]

    def update_alarms(self):
        for i in range(0, 14):
            if self.alarms_list[i] > 0:
                self.alarms_list[i] -= 1
            if self.alarms_list[i] == 0:
                if callable(getattr(self.__class__, "Alarm_" + str(i))):
                    alarm_func = getattr(self.__class__, "Alarm_" + str(i))
                    alarm_func(self)
                    self.alarms_list[i] = -1

    # inherited class should override
    def Alarm_0(self):
        pass

    # inherited class should override
    def Alarm_1(self):
        pass

    # inherited class should override
    def Alarm_2(self):
        pass

    # inherited class should override
    def Alarm_3(self):
        pass

    # inherited class should override
    def Alarm_4(self):
        pass

    # inherited class should override
    def Alarm_5(self):
        pass

    # inherited class should override
    def Alarm_6(self):
        pass

    # inherited class should override
    def Alarm_7(self):
        pass

    # inherited class should override
    def Alarm_8(self):
        pass

    # inherited class should override
    def Alarm_9(self):
        pass

    # inherited class should override
    def Alarm_10(self):
        pass

    # inherited class should override
    def Alarm_11(self):
        pass

    # inherited class should override
    def Alarm_12(self):
        pass

    # inherited class should override
    def Alarm_13(self):
        pass

    # inherited class should override
    def Alarm_14(self):
        pass
