from pygame.sprite import Group, GroupSingle

# https://stackoverflow.com/questions/70516673/how-does-pygame-sprite-group-know-which-sprite-group-to-call-also-calling-the
# Sprite.kill() removes the sprite from all of its groups

def instance_change(self, obj, perf, sprGroup):
    if perf == True:
        self.destroy()
    if isinstance(sprGroup, GroupSingle):
        sprGroup.add(obj)
    elif isinstance(sprGroup, Group):
        self.kill()
        sprGroup.add(obj)
    if perf == True:
        obj.create()
    # copy position
    obj.rect.center = self.rect.center
