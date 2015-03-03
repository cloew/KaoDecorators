from kao_decorators import smart_defaults, Default
import sys

@smart_defaults(Default('val', provider=lambda *args, **kwargs: {}))
def a(val={}, other='a'):
    if 1 in val:
        val[1] = val[1]+1
    else:
        val[1] = 1
    return val[1]
    
def b():
    return a(val=None)

def c(val=None):
    return a(val=val)
    
class A:
    
    def __init__(self, val):
        self.val = val
        
    # @smart_defaults(Default('something', provider=lambda self, *args, **kwargs: self.val))
    @smart_defaults(Default('something', field="val"))
    def doSomething(self, something=None):
        return something

def main(args):
    """ Run the main file """
    for i in range(3):
        print a()
        
    print b()
    print c()
    print c(val={})
    print a(None)
    print A(1).doSomething(2)
    print A(1).doSomething()
    print A(1).doSomething(None)
    print A(1).doSomething(something=3)

if __name__ == "__main__":
    main(sys.argv[1:])