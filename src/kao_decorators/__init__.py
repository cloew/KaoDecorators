
def lazy_property(fn):
    """ Convert function into a property where the function is 
        only called the first time the property is accessed """
    varName = "__{0}".format(fn.__name__)
    def lazyLoad(self):
        if not hasattr(self, varName):
            setattr(self, varName, fn(self))
        return getattr(self, varName)
    return property(lazyLoad)
    
    
def proxy_for(fieldName, attrs):
    """ Add properties for the attrs on the provided field to 
        hide interaction from a class to an internal component """
    def addProxyData(cls):
        def add_property(cls, attr):
            def setter(self, v):
                setattr(getattr(self, fieldName), attr, v)
            def getter(self):
                return getattr(getattr(self, fieldName), attr)
            setattr(cls, attr, property(getter, setter))
            
        for attr in attrs:
            add_property(cls, attr)
        return cls
    return addProxyData