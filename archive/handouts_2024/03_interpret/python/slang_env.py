import slang_parser
import slang_stdlib


class Env:
    """An environment/scope in which variables are defined"""

    def __init__(self, outer, poundF, poundT, empty):
        """Construct an environment.  We need a single global value for false,
        for true, and for empty.  We optionally have a link to an enclosing
        scope"""
        self.outer = outer
        self.map = {}
        self.poundF = poundF
        self.poundT = poundT
        self.empty = empty

    def put(self, key, val):
        """Unconditionally put a key into this environment"""
        self.map[key] = val

    def get(self, key):
        """Look up the value for a given key; recurse to outer environments as
        needed.  Throw an exception on failure."""
        return self.map[key] if key in self.map.keys() else self.outer.get(key)

    def update(self, key, val):
        """Update a key's value **in the scope where it is defined**"""
        if self.map.get(key) != None:
            self.map[key] = val
        else:
            self.outer.update(key, val)


def makeDefaultEnv():
    """Create a default environment by mapping all the built-in names (true,
    false, empty list, and the built-in functions)"""
    poundF = slang_parser.BoolNode(False)
    poundT = slang_parser.BoolNode(True)
    empty = slang_parser.ConsNode(None, None)
    e = Env(None, poundF, poundT, empty)
    # [mfs] Still a lot to do here:
    slang_stdlib.addMathFuncs(e)
    slang_stdlib.addListFuncs(e)
    slang_stdlib.addStringFuncs(e)
    slang_stdlib.addVectorFuncs(e)
    return e


def makeInnerEnv(outer):
    """Create an inner scope that links to its parent"""
    return Env(outer, outer.poundF, outer.poundT, outer.empty)
