import copy
import inspect

def get_default_args(func):
    """
    returns a dictionary of arg_name:default_values for the input function
    """
    args, varargs, keywords, defaults = inspect.getargspec(func)
    return dict(zip(reversed(args), reversed(defaults)))
    
    
class Default:
    """ Represents a default argument """
    
    def __init__(self, argument, perInstance=False):
        """ Initialize the default """
        self.argument = argument
        self.perInstance = perInstance
        
    def shouldUseDefault(self, kwargs):
        """ Return if the default value should be used """
        return self.argument in kwargs and kwargs[self.argument] is None
        
    def setDefault(self, kwargs, defaults):
        """ Return get the default value for the argument """
        kwargs[self.argument] = self.getDefault(defaults)
        
    def getDefault(self, defaults):
        """ Return get the default value for the argument """
        return defaults[self.argument]
        
class PerCallDefault(Default):
    """ Represents a default that should be copied for each execution of the function """
    
    def shouldUseDefault(self, kwargs):
        """ Return if the default value should be used """
        return Default.shouldUseDefault(self, kwargs) or self.argument not in kwargs
        
    def getDefault(self, defaults):
        """ Return get the default value for the argument """
        return copy.deepcopy(defaults[self.argument])

def smart_defaults(*args):
    """ Set the given arguments to be used as smart properties that 
        can be set to None and then set to the actual default value """
    defaults = [Default(arg) if type(arg) is str else arg for arg in args]
    def getFnDefaults(fn):
        defaultArgs = get_default_args(fn)
        def setKwargs(*args, **kwargs):
            for default in defaults:
                if default.shouldUseDefault(kwargs):
                    default.setDefault(kwargs, defaultArgs)
            return fn(*args, **kwargs)
        return setKwargs
    return getFnDefaults