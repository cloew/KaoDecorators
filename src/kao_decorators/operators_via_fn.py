
def operators_via_fn(fn):
    """ Add the operators by comparing the results from the given function """
    def addOperators(cls):
        class OperatorOverloads(cls):
            def __eq__(self, other):
                return fn(self) == fn(other)
                
            def __ne__(self, other):
                return fn(self) != fn(other)
                
            def __lt__(self, other):
                return fn(self) < fn(other)
                
            def __gt__(self, other):
                return fn(self) > fn(other)
                
            def __le__(self, other):
                return fn(self) <= fn(other)
                
            def __ge__(self, other):
                return fn(self) >= fn(other)
        return OperatorOverloads
    return addOperators