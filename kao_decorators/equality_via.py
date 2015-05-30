
def equality_via(*attrs):
    """ Decorator to add equality comparisons to a class via the provided attributes """
    def addEq(cls):
        def equals(self, other):
            if any([not hasattr(other, attr) for attr in attrs]):
                return NotImplemented
            else:
                return all([getattr(self, attr) == getattr(other, attr) for attr in attrs])
                    
        cls.__eq__ = equals
        return cls
    return addEq