import pygame
from pygame.sprite import Group, GroupSingle

# Fast collision detection, returning True / False
def place_meeting(self, x, y, sprGrp):
    sourceWithMask = False
    targetsWithMask = 0

    if not hasattr(self, 'mask'):
        sourceWithMask = True

    for sprTarget in sprGrp:
        if hasattr(sprTarget, 'mask'):
            targetsWithMask = targetsWithMask + 1

    # simplest case
    if not sourceWithMask and targetsWithMask == 0:
        # source has no mask and not any targets are with mask
        original_x = self.x
        original_y = self.y
        self.x = x
        self.y = y
        retVal = pygame.sprite.spritecollideany(self, sprGrp, collided = None)
        self.x = original_x
        self.y = original_y
        if retVal == None:
            return False
        else:
            return True
    else:
        # source or any targets are using masks... use slowest
        original_x = self.x
        original_y = self.y
        self.x = x
        self.y = y        
        retVal = pygame.sprite.spritecollideany(self, sprGrp, pygame.sprite.collide_mask)
        self.x = original_x
        self.y = original_y
        if retVal == None:
            return False
        else:
            return True

# Fast collision detection, for single collision, returning None / Object
def instance_place(self, x, y, sprGrp):    
    sourceWithMask = False
    targetsWithMask = 0

    if not hasattr(self, 'mask'):
        sourceWithMask = True

    for sprTarget in sprGrp:
        if hasattr(sprTarget, 'mask'):
            targetsWithMask = targetsWithMask + 1

    # for simple rect (without indicated by having a mask)
    if not sourceWithMask and targetsWithMask == 0:
        original_x = self.x
        original_y = self.y
        self.x = x
        self.y = y
        retVal = pygame.sprite.spritecollideany(self, sprGrp, collided = None)
        self.x = original_x
        self.y = original_y
        return retVal
    else:
        original_x = self.x
        original_y = self.y
        self.x = x
        self.y = y
        retVal = pygame.sprite.spritecollideany(self, sprGrp, pygame.sprite.collide_mask)
        self.x = original_x
        self.y = original_y
        return retVal

# For check_n_invoke_collisions, multiple collisions
def instance_place_all(self, x, y, sprGrp):   
    sourceWithMask = False
    targetsWithMask = 0

    if not hasattr(self, 'mask'):
        sourceWithMask = True

    for sprTarget in sprGrp:
        if hasattr(sprTarget, 'mask'):
            targetsWithMask = targetsWithMask + 1

    # simplest case
    if not sourceWithMask and targetsWithMask == 0:
        # source has no mask and not any targets are with mask
        original_x = self.x
        original_y = self.y
        self.x = x
        self.y = y
        retVals = pygame.sprite.spritecollide(self, sprGrp, False, collided = None)
        self.x = original_x
        self.y = original_y
        return retVals
    else:
        # source or any targets are using masks... use slowest
        original_x = self.x
        original_y = self.y
        self.x = x
        self.y = y
        retVals = pygame.sprite.spritecollide(self, sprGrp, False, pygame.sprite.collide_mask)
        self.x = original_x
        self.y = original_y
        return retVals

# Supports multiple collisions with all groups and with "other"
def check_n_invoke_collisions(self, *srpArgv):
    for sprArg in srpArgv:
        spritesAll = instance_place_all(self, self.x, self.y, sprArg)
        for spr in spritesAll:
            # Takes class name of the collided sprite, adding on_ for it (to not mess python)
            callfunc = "on_" + type(spr).__name__
            if hasattr(self, callfunc):
                if callable(getattr(self.__class__, callfunc)):
                    collision_func = getattr(self.__class__, callfunc)
                    collision_func(self, other=spr)