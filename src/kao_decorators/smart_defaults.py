import copy
import inspect

class FunctionMetadata:
    """ Represents a functions metadata """
    
    def __init__(self, func):
        """ Initialize the metadata """
        self.args, varargs, keywords, defaults = inspect.getargspec(func)
        self.defaults = dict(zip(reversed(self.args), reversed(defaults)))
        
    def getArgIndex(self, arg):
        """ Return the inline argument index for a given argument """
        return self.args.index(arg)
        
class SmartArg:
    """ Helper class to handle interacting with a particular argument """
    
    def __init__(self, argName, funcMetadata):
        """ Initialize the smart argument with its name and the metadata of the function """
        self.argName = argName
        self.inlineIndex = funcMetadata.getArgIndex(self.argName)
        
    def isProvided(self, args, kwargs):
        """ Return if this argument has been specified in the given arguments """
        return self.argName in kwargs or len(args) > self.inlineIndex
        
    def getValue(self, args, kwargs):
        """ Return the argument value """
        if len(args) > self.inlineIndex:
            return args[self.inlineIndex]
        else:
            return kwargs[self.argName]
        
    def setValue(self, args, kwargs, newValue):
        """ Set the argument to the specified value """
        if len(args) > self.inlineIndex:
            args[self.inlineIndex] = newValue
        else:
            kwargs[self.argName] = newValue
            
class Default:
    """ Represents a default argument """
    
    def __init__(self, argument):
        """ Initialize the default """
        self.argName = argument
        
    def setMetadata(self, metadata):
        """ Set the default's metadata """
        self.argument = SmartArg(self.argName, metadata)
        self.metadata = metadata
        
    def shouldUseDefault(self, args, kwargs):
        """ Return if the default value should be used """
        return self.argument.isProvided(args, kwargs) and self.argument.getValue(args, kwargs) is None
        
    def setDefault(self, args, kwargs):
        """ Return get the default value for the argument """
        self.argument.setValue(args, kwargs, self.getDefault())
        
    def getDefault(self):
        """ Return get the default value for the argument """
        return self.metadata.defaults[self.argument.argName]
        
class PerCallDefault(Default):
    """ Represents a default that should be copied for each execution of the function """
    
    def shouldUseDefault(self, args, kwargs):
        """ Return if the default value should be used """
        return Default.shouldUseDefault(self, args, kwargs) or not self.argument.isProvided(args, kwargs)
        
    def getDefault(self):
        """ Return get the default value for the argument """
        return copy.deepcopy(Default.getDefault(self))

def smart_defaults(*args):
    """ Set the given arguments to be used as smart properties that 
        can be set to None and then set to the actual default value """
    defaults = [Default(arg) if type(arg) is str else arg for arg in args]
    def getFnDefaults(fn):
        metadata = FunctionMetadata(fn)
        [default.setMetadata(metadata) for default in defaults]
        def setKwargs(*args, **kwargs):
            args = list(args)
            for default in defaults:
                if default.shouldUseDefault(args, kwargs):
                    default.setDefault(args, kwargs)
            return fn(*args, **kwargs)
        return setKwargs
    return getFnDefaults