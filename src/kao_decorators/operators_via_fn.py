
def operators_via_fn(fn):
    """ Add the operators by comparing the results from the given function """
    def addOperators(cls):
        def equals(self, other):
            return fn(self) == fn(other)
            
        def notequals(self, other):
            return fn(self) != fn(other)
            
        def lessthan(self, other):
            return fn(self) < fn(other)
            
        def greaterthan(self, other):
            return fn(self) > fn(other)
            
        def lessthanequals(self, other):
            return fn(self) <= fn(other)
            
        def greaterthanequals(self, other):
            return fn(self) >= fn(other)
            
        cls.__eq__ = equals
        cls.__ne__ = notequals
        cls.__lt__ = lessthan
        cls.__gt__ = greaterthan
        cls.__le__ = lessthanequals
        cls.__ge__ = greaterthanequals
        
        return cls
    return addOperators