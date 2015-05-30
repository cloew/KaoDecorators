
def lazy_property(fn):
    """ Convert function into a property where the function is 
        only called the first time the property is accessed """
    varName = "__{0}".format(fn.__name__)
    def lazyLoad(self):
        if not hasattr(self, varName):
            setattr(self, varName, fn(self))
        return getattr(self, varName)
    return property(lazyLoad)