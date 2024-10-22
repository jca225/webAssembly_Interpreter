from settings import *

class Env:
    """Definitions are referenced with zero-based indices. Each class of definitions has its own index space, as distinguished
    by the following classes"""

    def __init__(self):
        # Unnamed indices are associated with the empty (\epsilon) entries in these lists
        self.types = {}
        self.funcs = {}
        self.tables = {}
        self.mems = {}
        self.globals = {}
        self.elems = {}
        self.data = {}
        self.typedefs = {}

    def _getContext(self, space):
        if space == "types":
            return self.types
        elif space == "funcs":
            return self.funcs
        elif space == "tables":
            return self.tables
        elif space == "mems":
            return self.mems
        elif space == "globals":
            return self.globals
        elif space == "data":
            return self.data
        elif space == "elems":
            return self.elems
        elif space == "typedefs":
            return self.typedefs

    def getIdentifierIndex(self, space, identifier):
        """Returns the index corresponding to the identifier"""
        if isinstance(identifier, str):
            for index,iteratedIdentifier in self._getContext(space).items():
                if iteratedIdentifier == identifier: return index
        elif isinstance(identifier, int):
            return identifier
    def addIdentifierIndex(self, space, identifier):
        """Add index corresponding to the identifier"""
        index = len(self._getContext(space))
        self._getContext(space)[index] = identifier
        return index

class Frame:
    def __init__(self):
        # Unnamed indices are associated with the empty (\epsilon) entries in these lists
        self.locals = {}
        self.labels = {}
        self.returns = []
        self.args = {}

    def returnArity(self):
        return len(self.returns)
    def setLocal(self, value):
        index = len(self.locals)
        self.locals[index] = value
    def setLocalValue(self, value, index):
        self.locals[index]['value'] = value
    def getLocal(self, index):
        return self.locals[index]['value']
    def addArg(self, arg):
        index = len(self.args)
        self.args[index] = arg
    def addReturn(self, valtype):
        self.returns.append(valtype)
    def argArity(self):
        return len(self.args)
    

class Label:
    def __init__(self, instructions, argumentArity, index, type):
        self.instructions = instructions
        self.argumentArity = argumentArity
        self.index = index
        self.type = type # BLOCK, LOOP
        self.continuation = []
        # If it is of type loop, then the continuation is all instructions leading up to the branch instruction
        if self.type == LOOP:
            # Loop through the instructions and while there is no branch instruction, add to the continuation
            for i in range(len(self.instructions)):
                self.continuation.append(self.instructions[i])
                if self.instructions[i]['type'] == BR or self.instructions[i]['type'] == BR_IF:
                    break
    
