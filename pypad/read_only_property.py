def _pass(s):
    pass

def read_only_property(fget):
    return property(fget, _pass, _pass)