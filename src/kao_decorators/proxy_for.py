
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