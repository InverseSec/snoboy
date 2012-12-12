from ctypes import c_ubyte, c_ushort

# how many cycles we've executed
ticks = 0


def add_ticks(t):
    global ticks
    ticks = ticks + t


def _register16(default=0):
    """Create a property around a c_ushort"""
    _value = c_ushort(default)

    def get(self):
        return _value.value

    def set(self, value):
        _value.value = value

    return property(get, set)


def _register(default=0):
    """Create a property around a c_ubyte."""
    _value = c_ubyte(default)

    def get(self):
        return _value.value

    def set(self, value):
        _value.value = value

    return property(get, set)


def _compound_register(upper, lower):
    """Return a property that provides 16-bit access to two registers."""
    def get(self):
        return (upper.fget(None) << 8) | lower.fget(None)

    def set(self, value):
        upper.fset(None, value >> 8)
        lower.fset(None, value)

    return property(get, set)


class Registers(object):
    A = _register()
    F = _register()
    B = _register()
    C = _register()
    D = _register()
    E = _register()
    H = _register()
    L = _register()
    BC = _compound_register(B, C)
    DE = _compound_register(D, E)
    HL = _compound_register(H, L)

    SP = _register16()
    PC = _register16()

    def __getitem__(self, index):
        return getattr(self, index)

    def __setitem__(self, index, value):
        setattr(self, index, value)
registers = Registers()

