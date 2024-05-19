import pygame, math

def ClampFloat(_f):
    return max(min(_f, 1000000), -1000000)

def Sqr( _x ):
    return _x**2

# Using:
#
# - Move to right (accelerating)
#       hspeed = get_hspeed() + 1
#       set_hspeed(hspeed)
#       calculate_position()
#
# - Move to up (accelerating)
#       vspeed = get_vspeed() - 1
#       set_vspeed(vspeed)
#       calculate_position()
#

class Object_trigonometric(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()

        x = pos_x
        y = pos_y
        direction = 0.0
        speed = 0.0
        hspeed = 0.0
        vspeed = 0.0

        friction = 0.0
        __friction = friction
        gravity = 0.0
        __gravity = gravity
        gravity_direction = 270.0
        __gravity_direction = gravity_direction

        __direction = direction
        __speed = speed
        __hspeed = hspeed
        __vspeed = vspeed

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]


    # hspeed property
    def	get_hspeed(self):
        return self.__hspeed

    def set_hspeed(self, _val):
        if (self.__hspeed == _val):
            return
        self.__hspeed = _val
        self.Compute_Speed1()

    def sethspeed(self, _val):
        if (self.hspeed == _val):
            return
        self.hspeed = _val
        self.Compute_Speed1()


    # vspeed property
    def get_vspeed(self):
        return self.__vspeed

    def set_vspeed(self, _val):
        if (self.__vspeed == _val):
            return
        self.__vspeed = _val
        self.Compute_Speed1()

    def setvspeed(self, _val):
        if (self.vspeed == _val):
            return
        self.vspeed = _val
        self.Compute_Speed1()


    # direction property
    def get_direction(self):
        return self.__direction

    def set_direction(self, _val):
        self.__direction = math.fmod(_val, 360.0)	
        self.Compute_Speed2()

    def setdirection(self, _val):
        self.direction = math.fmod(_val, 360.0)
        while (self.direction < 0.0):
            self.direction += 360.0
        self.Compute_Speed2()


    # speed property
    def get_speed(self):
        return self.__speed

    def set_speed(self, _val):
        if (self.__speed == _val):
            return
        self.__speed = _val
        self.Compute_Speed2()

    def setspeed(self, _val):
        if (self.speed == _val):
            return
        self.speed = _val
        self.Compute_Speed2()


    def Compute_Speed2(self):
        self.__hspeed = self.speed * ClampFloat(math.cos(self.direction * 0.0174532925))
        self.__vspeed = -self.speed * ClampFloat(math.sin(self.direction * 0.0174532925))

        # Round it down
        if (abs(self.__hspeed - round(self.__hspeed)) < 0.0001):
            self.__hspeed = round(self.__hspeed)
        if (abs(self.__vspeed - round(self.__vspeed)) < 0.0001):
            self.__vspeed = round(self.__vspeed)


    # friction property
    def get_friction(self):
        return self.__friction

    def set_friction(self, _val):
        if (self.__friction == _val):
            return
        self.__friction = _val


    # gravity property
    def get_gravity(self):
        return self.__gravity

    def set_gravity(self, _val):
        if (self.__gravity == _val):
            return
        self.__gravity = _val


    # gravity_direction property
    def get_gravity_direction(self):
        return self.__gravity_direction

    def set_gravity_direction(self, _val):
        if (self.__gravity_direction == _val):
            return
        self.__gravity_direction = _val


    def AdaptSpeed(self):
        if(self.get_hspeed() > 0):
            self.speed = self.get_hspeed()

        # deal with friction
        if (self.friction != 0.0):
            ns = 0.0
            if (self.speed > 0):
                ns = self.speed - self.friction
            else:
                ns = self.speed + self.friction

            if ((self.speed > 0) and (ns < 0)):
                self.speed = 0
            elif ((self.speed < 0) and (ns > 0)):
                self.speed = 0
            elif (self.speed != 0):
                self.speed = ns
                self.set_hspeed(self.speed)

            if( ns > 0):
                self.Compute_Speed2()
                if(self.__speed != 0):
                    self.__hspeed += self.__speed * ClampFloat(math.cos(self.__direction * 0.0174532925))
                    self.__vspeed -= self.__speed * ClampFloat(math.sin(self.__direction * 0.0174532925))
            else:
                # when nominal speed is zero, also set hspeed to zero
                if(self.get_hspeed() > 0):
                    self.set_hspeed(0)

        # deal with gravity: influencing both instance speed and its direction
        if (self.gravity != 0):
            self.AddTo_Speed(self.gravity_direction, self.gravity)

    def AddTo_Speed(self, _dir, _amount):
        self.hspeed += self._amount * ClampFloat(math.cos( self._dir * 0.0174532925))
        self.vspeed -= self._amount * ClampFloat(math.sin( self._dir * 0.0174532925))
        # will not add "__hspeed += hspeed" since it breaks friction from working
        self.__vspeed += self.vspeed
        self.Compute_Speed1()

    def Compute_Speed1(self):
        # direction
        if (self.hspeed == 0):
            if (self.vspeed > 0):
                self.__direction = 270
            elif (self.vspeed < 0):
                self.__direction = 90
            else:
                self.__direction = 0
        else:
            dd = ClampFloat(180 * (math.atan2(self.vspeed, self.hspeed)) / math.pi)
            if (dd <= 0):
                self.__direction = -dd
            else:   
                self.__direction = 360.0 - dd

        # direction
        if (abs(self.__direction - round(self.__direction)) < 0.0001):
            self.__direction = round(self.__direction)
        self.__direction = math.fmod(self.__direction, 360.0)

        # speed
        self.__speed = math.sqrt(Sqr(self.hspeed) + Sqr(self.vspeed));
        if (abs(self.speed - round(self.speed)) < 0.0001):
            self.__speed = round(self.__speed)

    def calculate_position(self):
        self.AdaptSpeed()
        if (self.get_hspeed() != 0 or self.get_vspeed() != 0):
            self.x += self.get_hspeed()
            self.y += self.get_vspeed()
