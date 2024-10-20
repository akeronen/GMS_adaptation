import pygame, sys
from collisions import *
from events_inherited import *

class Object_Collisions():
    collision_groups = []

    def __init__(self):
        pass

    # Add another collision group to this object (if interacts with it)
    def add_interacting_collision_group(self, sprGroup: pygame.sprite.Group):
        self.collision_groups.append(sprGroup)

    # Add multiple collision groups at the same time
    def add_interacting_collision_groups(self, *sprGroups: pygame.sprite.Group):
        for sprArg in sprGroups:
            self.collision_groups.append(sprArg)

    # Actual collision checking and invoking
    def check_n_invoke_collisions(self, arrayOfCGs):
        for colGroup in arrayOfCGs:
            spritesAll = instance_place_all(self, self.x, self.y, colGroup)
            for spr in spritesAll:
                # take class name of the collided sprite, adding on_ for it (to not mess python)
                callfunc = "on_" + type(spr).__name__
                if hasattr(self, callfunc):
                    if callable(getattr(self.__class__, callfunc)):
                        collision_func = getattr(self.__class__, callfunc)
                        collision_func(self, other=spr)
                else:
                    print("missing: " + callfunc)

    # Needs to be implement in every super class to complete whole chain
    def check_collisions(self):
        events_inherited(self)
        # check collisions on this object
        check_n_invoke_collisions(self.collision_groups)
