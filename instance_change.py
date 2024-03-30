from pygame.sprite import Group, GroupSingle

def instance_change(self, obj, perf, sprGroup):
    if perf == True:
        self.destroy()
    if isinstance(sprGroup, GroupSingle):
        sprGroup.add(obj)
    elif isinstance(sprGroup, Group):
        # ToDo
        pass
    if perf == True:
        obj.create()
    # copy position
    obj.rect.center = self.rect.center
