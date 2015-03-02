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
            
class ValueProvider:
    """ Returns a value from a method """
    
    def __init__(self, method):
        """ Initialize the Value Provider """
        self.getValue = method
        
    def shouldProvide(self, argument, args, kwargs):
        """ Return if the Value Provider should be used """
        return (argument.isProvided(args, kwargs) and argument.getValue(args, kwargs) is None) or not argument.isProvided(args, kwargs)
            
class FieldProvider:
    """ Returns a value from a field on the first argument (typically self) """
    
    def __init__(self, fieldName):
        """ Initialize the Value Provider """
        self.fieldName = fieldName
        
    def shouldProvide(self, argument, args, kwargs):
        """ Return if the Value Provider should be used """
        return (argument.isProvided(args, kwargs) and argument.getValue(args, kwargs) is None) or not argument.isProvided(args, kwargs)
        
    def getValue(self, obj, *args, **kwargs):
        """ Return the value for this default """
        return getattr(obj, self.fieldName)
        
class DefaultProvider:
    """ Returns a value from the function defaults """
    
    def __init__(self, argument, metadata):
        """ Initialize the Value Provider """
        self.argument = argument
        self.metadata = metadata
        
    def shouldProvide(self, argument, args, kwargs):
        """ Return if the Value Provider should be used """
        return argument.isProvided(args, kwargs) and argument.getValue(args, kwargs) is None
        
    def getValue(self, *args, **kwargs):
        """ Return the value for this default """
        return self.metadata.defaults[self.argument.argName]
        
class PerCallProvider(DefaultProvider):
    """ Returns a copy of the value from the function defaults """
        
    def shouldProvide(self, argument, args, kwargs):
        """ Return if the Value Provider should be used """
        return DefaultProvider.shouldProvide(self, argument, args, kwargs) or not argument.isProvided(args, kwargs)
        
    def getValue(self, *args, **kwargs):
        """ Return the value for this default """
        return copy.deepcopy(DefaultProvider.getValue(self, *args, **kwargs))
            
class Default:
    """ Represents a default argument """
    
    def __init__(self, argument, perCall=False, field=None, provider=None):
        """ Initialize the default """
        self.argName = argument
        self.perCall = perCall
        self.field = field
        self.provider = provider
        
class BoundDefault:
    """ Represents a default argument bound to its function metadata """
        
    def __init__(self, defaultData, metadata):
        """ Set the default's metadata """
        self.argument = SmartArg(defaultData.argName, metadata)
        self.metadata = metadata
        
        if defaultData.provider is not None:
            self.provider = ValueProvider(defaultData.provider)
        elif defaultData.field is not None:
            self.provider = FieldProvider(defaultData.field)
        elif defaultData.perCall:
            self.provider = PerCallProvider(self.argument, metadata)
        else:
            self.provider = DefaultProvider(self.argument, metadata)
        
    def shouldUseDefault(self, args, kwargs):
        """ Return if the default value should be used """
        return self.provider.shouldProvide(self.argument, args, kwargs)
        
    def setDefault(self, args, kwargs):
        """ Return get the default value for the argument """
        self.argument.setValue(args, kwargs, self.provider.getValue(*args, **kwargs))

def smart_defaults(*args):
    """ Set the given arguments to be used as smart properties that 
        can be set to None and then set to the actual default value """
    defaults = [Default(arg) if type(arg) is str else arg for arg in args]
    def getFnDefaults(fn):
        metadata = FunctionMetadata(fn)
        boundDefaults = [BoundDefault(default, metadata) for default in defaults]
        def setKwargs(*args, **kwargs):
            args = list(args)
            for default in boundDefaults:
                if default.shouldUseDefault(args, kwargs):
                    default.setDefault(args, kwargs)
            return fn(*args, **kwargs)
        return setKwargs
    return getFnDefaults