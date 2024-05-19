import pygame, math
# Define a 2d Vector
vector = pygame.math.Vector2


# Using:
#
# - Move to right (accelerating, by an impulse value)
#       hspeed = 5
#       calculate_position()
#
# - Move to up (accelerating, by an impulse value)
#       vspeed = -13.5
#       calculate_position()
#
# - Restrict hspeed or vspeed
#       if(velocity.x > 5):
#           hspeed_restrict = 5
#       if(velocity.y > 25):
#           vspeed_restrict = 25
#
# - Stop falling due to gravity
#       velocity.y = 0
#

class Object_vector(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()

        x = pos_x
        y = pos_y
        old_x = x
        old_y = y

        direction = 0.0
        speed = 0.0

        hspeed = 0.0                    # working as an impulse force, resets back to 0
        vspeed = 0.0                    # working as an impulse force, resets back to 0
        old_hspeed = 0.0
        old_vspeed = 0.0
        hspeed_restrict = 0.0           # working as a restricting hspeed scale to set value
        vspeed_restrict = 0.0           # working as a restricting vspeed scale to set value

        friction = 0                    # "sane" value range is 0 .. 0.49
        gravity = 0.0
        gravity_direction = 270.0       # NOT SUPPORTED

        # Kinematic Vectors (x,y)
        position = vector(x,y)
        velocity = vector(0,0)
        acceleration = vector(0,0)

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def reset_internal_speeds(self):
        self.hspeed = self.vspeed = self.hspeed_restrict = self.vspeed_restrict = 0.0

    def calculate_position(self):
        # Gravity taken into use
        if(self.gravity != 0):
            self.acceleration = vector(0, self.gravity)
        else:
            self.acceleration = vector(0, 0)

        if(self.hspeed != 0):
            self.velocity.x += self.hspeed

        # Calculate new kinematics
        self.acceleration.x += round(self.velocity.x * self.friction, 2)
        if(self.vspeed == 0):
            self.velocity += self.acceleration
        else:
            self.velocity = vector(self.velocity.x, self.vspeed)

        if(self.friction != 0):
            self.velocity.x *= self.friction      # otherwise friction has no effect after impulse was given
            self.velocity.x = round(self.velocity.x, 2)

        # Store old position
        self.old_x = self.x
        self.old_y = self.y

        new_hspeed = vector(self.velocity.x + 0.5 * self.acceleration.x, 0)
        new_vspeed = vector(0, self.velocity.y + 0.5 * self.acceleration.y)
        if(self.hspeed_restrict != 0):
            if(new_hspeed.x != 0):
                new_hspeed.scale_to_length(self.hspeed_restrict)
            else:
                new_hspeed.x = self.hspeed_restrict
        if(self.vspeed_restrict != 0):
            if(new_vspeed.y != 0):
                new_vspeed.scale_to_length(self.vspeed_restrict)
            else:
                new_vspeed.y = self.vspeed_restrict
        result_vec = vector(new_hspeed.x, new_vspeed.y)

        # Original secret sauce was: position += velocity + 0.5 * acceleration
        self.position += result_vec

        # Calculated speeds
        result_hspeed = self.position.x - self.old_x
        result_vspeed = self.position.y - self.old_y
    
        # Set new coordinates
        self.x = self.position.x
        self.y = self.position.y

        # calculate direction & speed
        # GMS style values:
        #           90
        #    179    |     1
        #   180 ---------- 0
        #    181    |    359
        #          270
        #

        # https://stackoverflow.com/questions/21483999/using-atan2-to-find-angle-between-two-vectors
        v1 = vector(self.old_x, self.old_y)
        v2 = vector(self.x, self.y)    
        v1tov2 = math.atan2(v1.y - v2.y, v2.x - v1.x)
        if (v1tov2 < 0):
            v1tov2 += 2 * math.pi
        self.direction = round(math.degrees(v1tov2), 2)
        self.speed = round(result_vec.length(), 2)

        # Store old
        self.old_hspeed = result_vec.x
        self.old_vspeed = result_vec.y
