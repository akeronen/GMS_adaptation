import pygame, sys
from collisions import *
from events_inherited import *

class Object_Collisions():
    collision_groups = {}

    def __init__(self):
        pass

    # Add another collision group to this object (if interacts with it)
    def add_interacting_collision_group(self, identifier, sprGroup: pygame.sprite.Group):
        self.collision_groups[identifier] = sprGroup

    # Add multiple collision groups at the same time
    def add_interacting_collision_groups(self, identifier, *sprGroups: pygame.sprite.Group):
        addedGroups = []
        for aGroup in sprGroups:
            addedGroups.append(aGroup)
        self.collision_groups[identifier] = addedGroups

    # Actual collision checking and invoking
    def check_collisions(self):
        for key, val in self.collision_groups.items():
            spritesAll = instance_place_all(self, self.x, self.y, val)
            for spr in spritesAll:
                callfunc = key
                if hasattr(self, callfunc):
                    if callable(getattr(self.__class__, callfunc)):
                        collision_func = getattr(self.__class__, callfunc)
                        collision_func(self, other=spr)
                else:
                    print("missing: " + callfunc)
