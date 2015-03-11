
def equality_via(*attrs):
    """ Decorator to add equality comparisons to a class via the provided attributes """
    def addEq(cls):
        class EqCls(cls):
            def __eq__(self, other):
                if any([not hasattr(other, attr) for attr in attrs]):
                    return NotImplemented
                else:
                    return all([getattr(self, attr) == getattr(other, attr) for attr in attrs])
        return EqCls
    return addEq