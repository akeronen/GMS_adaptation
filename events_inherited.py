import inspect

# https://stackoverflow.com/questions/40652688/how-to-access-globals-of-parent-module-into-a-sub-module

def events_inherited(self):
    for parentClass in self.__class__.__bases__:
        # get our frame
        this_frame = inspect.currentframe()
        # get caller's frame
        caller_frame = this_frame.f_back
        # lookup caller globals
        m = caller_frame.f_globals.get (parentClass.__name__)
        if m:
            func = getattr(m, inspect.stack()[1][3])
            # if method found call it
            if func:
                func(self)
                return
