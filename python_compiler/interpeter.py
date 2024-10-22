from settings import *
from env import *
import copy
"""
def constructStore():
    return {"funcAddr": [], "tableAddr": [], "memAddr": [], "globalAddr": [], "elemAddr": [], "dataAddr": [], "externAddr": []}
def constructModuleInstance():
    return {"types": [], "funcAddr": [], "tableAddr": [], "memAddr": [], "globalAddr": [], "elemAddr": [], "dataAddr": [], "exports": []}
def constructFuncInstance(functype, moduleinst, funcCode, frame):
    return {"type": functype, "module":moduleinst, "code": funcCode, "frame": frame}
def constructExportInstance(name, type, externval):
    return {"name": name, "type": type, "externval":externval}
def constructMemoryInstance(memtype): 
    return {"type": memtype, "data": [0] * int(memtype['min']) * 65536}
def constructGlobalInstance(globaltype, val):
    return {"globaltype": globaltype, "val": val}
def constructTableInstance(type):
    return {"type": type, "references": []}
def constructActivationFrame(returnArity, locals, moduleInstanceRef):
    return {"returnArity": returnArity, "locals": locals, "moduleInstanceRef": moduleInstanceRef}
"""
class Stack:
    """Stores elements that are processed in LIFO fashion (Last-In First-Out)"""
    def __init__(self):
        self.stack = []
    def peek(self):
        return self.stack[0]
    def pop(self):
        return self.stack.pop(0)
    def push(self,e):
        self.stack.insert(0,e)
    def search(self, e):
        if e in self.stack: return e
        return None
    def empty(self):
        if self.stack == []:
            return True
        return False

class Interpreter:
    def __init__(self):
        self.stack = Stack()

    def instantiate(self, ast):
        self.funcInstances = {}
        self.typeInstances = {}
        self.exportInstances = {}
        self.importInstances = {}
        """We first must instantiate an instance to run any functions within it"""
        self.ast = ast
        self.globalEnv = self.ast['env']
        """We take as input an AST dictionary. """
        for field in self.ast['fields']:
            # Ignore types for now as part of our quick and dirty implementation
            if field['type'] == TYPE:
                self.typeInstances[field['id']] = field
            # Append func to auxiliary list containing all our functions
            elif field['type'] == FUNC:
                self.funcInstances[field['id']] = field
            elif field['type'] == IMPORT:
                pass
            elif field['type'] == EXPORT:
                self.exportInstances[field['id']] = field
 

    def callExtern(self, funcname, opType, *args):
        """User calls an exported function."""
        
        for exportId, export in self.exportInstances.items():
            # Evaluate the export if it is found
            if funcname != export['name']:
                continue
            if opType == FUNC:
                function = self.funcInstances[export['id']]
                # Push external arguments onto the stack
                for arg in args:
                    self.stack.push(arg)
                self.callFunc(function)
                for result in self.stack.stack:
                    return result
                

    def callFunc(self, funcInstance):
        # On each function call, we create a new local frame from our base frame that will hold the current instantiation's
        # metadata
        frame = copy.deepcopy(funcInstance['frame'])

        # Pop values from stack and store them on the local activation frame.
        # Note that these are parameters so we start at index 0.
        for i in range(frame.argArity()):
            frame.setLocalValue(self.stack.pop(), i)
        
        # Push the frame onto the stack
        self.stack.push(frame)
        # Parse the instructions
        self.enterInstructionSequence(funcInstance['instr'], frame)
        # Determine the number of values returned by the function
        returnArity = frame.returnArity()
        # Save the return values and pop from the stack
        returns = []

        for i in range(returnArity):
            returns.append(self.stack.pop())       
        # pop activation frame for that function
        poppedFrame = self.stack.pop()
        # Push return values back onto the stack
        for result in returns:
            self.stack.push(result)
    
    def enterInstructionSequence(self, code, frame):
        for i in range(len(code)):
            instruction = code[i]
            if not self.interpretInstruction(instruction, frame):
                return False

    def interpretInstruction(self, instruction, frame):
        """
            False -> exit out of function
            True -> stay in function
        """
        if instruction['type'] == BLOCK:
            # Instatiate label object
            label = Label(instruction["instructions"], 0, 0, BLOCK)
            # Push label onto stack
            self.stack.push(label)
            # Enter constroled instruction sequence
            return self.interpretStructuredControlInstructions(frame, label)
        elif instruction['type'] == LOOP:
            # Instatiate label object
            label = Label(instruction["instructions"], 0, 0, LOOP)
            # Push label onto stack
            self.stack.push(label)
            # Enter constroled instruction sequence. 
            # If it returns false, then exit out of the instruction sequence
            return self.interpretStructuredControlInstructions(frame, label)
        elif instruction['type'] == LOCALGET:
            self.stack.push(frame.getLocal(int(instruction['operand'])))
            return True      
        elif instruction['type'] == LOCALSET:
            frame.setLocalValue(self.stack.pop(), int(instruction['operand']))
            return True
        elif instruction['type'] == LOCALTEE:
            frame.setLocalValue(self.stack.peek(), int(instruction['operand'])) 
            return True   
        elif instruction['type'] == CALL:
            # Get address of function in our store
            functionAddress = self.globalEnv.getIdentifierIndex("funcs", instruction['operand'])
            function = self.funcInstances[functionAddress]           
            self.callFunc(function)
            return True
        elif instruction['type'] == CONST:
            self.stack.push(int(instruction['operand']))
            return True
        elif instruction['type'] == ADD:
            self.stack.push(self.stack.pop() + self.stack.pop())
            return True
        elif instruction['type'] == GE_S:
            second = self.stack.pop()
            first = self.stack.pop()
            self.stack.push(int(first >= second))
            return True
        elif instruction['type'] == SUB:
            second = self.stack.pop()
            first = self.stack.pop()
            self.stack.push(first - second)
            return True
        elif instruction['type'] == GT_U:
            # Convert both to unsigned
            second = self.stack.pop()
            first = self.stack.pop()
            if first < 0:
                first += (1 << 32)
            if second < 0:
                second += (1 << 32)
            self.stack.push(int(first > second))
            return True
        elif instruction['type'] == EQZ:
            self.stack.push(int(self.stack.pop() == 0))
            return True
        elif instruction['type'] == EQ:
            self.stack.push(int(self.stack.pop() == self.stack.pop()))
            return True
        elif instruction['type'] == OR:
            self.stack.push(int(self.stack.pop() or self.stack.pop()))
            return True
        elif instruction['type'] == LT_S:
            second = self.stack.pop()
            first = self.stack.pop()
            self.stack.push(int(first < second))
            return True
        elif instruction['type'] == GE_S:
            second = self.stack.pop()
            first = self.stack.pop()
            self.stack.push(int(first >= second))
            return True
        elif instruction['type'] == DROP:
            self.stack.pop()
            return True
        elif instruction['type'] == RETURN:
            return False
        elif instruction['type'] in [BR, BR_IF]:
            return False

    
    def interpretStructuredControlInstructions(self, frame, label):
        """
            True -> jump to position after "end" keyword
            False -> exit out of function call itself
        """
        i=0
        while i < len(label.instructions):
            instruction = label.instructions[i]
            i+=1
            # If the instruction type was not a branch instruction
            if self.interpretInstruction(instruction, frame):
                continue
            elif instruction['type'] == BR_IF:
                # If the result is True
                if self.stack.pop() != 0:
                    for __ in range(instruction['operand'] + 1): # Loop through l + 1 (l is our operand)
                        # I.e., while the top of a stack is a value
                        while not isinstance(self.stack.peek(), Label) and not isinstance(self.stack.peek(), Frame): 
                            self.stack.pop()
                        # Pop the label from the stack
                        poppedLabel = self.stack.pop()
                    if label.type==LOOP: 
                        self.stack.push(poppedLabel)
                        i = 0 # Jump to the continuation of L (for a loop, this means going to the original loop index)
                    elif label.type==BLOCK: 
                        return True # Jump to the continuation of L (for a block, this means breaking out of the current block)
                # If the result is false, continue normally
                else:
                    continue
            # If it is not a branch instruction but we returned false, then it implies we must break out of all the structured control instructions.
            # This implies we return from our function call, and we must configure the stack appropriately
            else:
                values = []
                # Pop all the values from the stack
                while not isinstance(self.stack.peek(), Frame) and not isinstance(self.stack.peek(), Label):
                    values.append(self.stack.pop())
                # Pop the label from the stack
                poppedLabel = self.stack.pop()
                # Push the values back onto the stack
                if len(values) == 0: return False
                elif len(values) == 1: self.stack.push(values[0])
                else:
                    for i in range(len(values) - 1, 0, -1):
                        self.stack.push(values[i])
                # Exit out of structured control sequence
                return False      
        # If we completed all of our instructions without a trap, abort, or return, then we can continue normally
        values = []
        # Pop all the values from the stack
        while not isinstance(self.stack.peek(), Frame) and not isinstance(self.stack.peek(), Label):
            values.append(self.stack.pop())
        # Pop the label from the stack
        poppedLabel = self.stack.pop()
        # Push the values back onto the stack
        if len(values) == 1: self.stack.push(values[0])
        else:
            for i in range(len(values) - 1, 0, -1):
                self.stack.push(values[i])
        return True


    """
    def enterInstructionSequence(self, code, frame):
        for i in range(len(code)):
            instruction = code[i]
            if instruction['type'] == LOCALGET:
                self.stack.push(frame['locals'][int(instruction['value'])]['val'])
            elif instruction['type'] == LOCALSET:
                val = self.stack.pop()
                frame['locals'][int(instruction['value'])]['val'] = val
            elif instruction['type'] == LOCALTEE:
                val = self.stack.pop()
                self.stack.push(val)
                frame['locals'][int(instruction['value'])]['val'] = val
            elif instruction['type'] == GLOBALGET:
                self.stack.push(int(self.store['globalAddr'][int(instruction['value'])]['val']))
            elif instruction['type'] == GLOBALSET:
                self.store['globalAddr'][int(instruction['value'])]['val'] = self.stack.pop()            
            elif instruction['type'] == CALL:
                addr = instruction['value']
                funcInst = self.store['funcAddr'][int(addr)]                  
                self.callFunc(funcInst)
            elif instruction['type'] == CONST:
                self.stack.push(int(instruction['value']))
            elif instruction['type'] == ADD:
                self.stack.push(self.stack.pop() + self.stack.pop())
            elif instruction['type'] == GE_S:
                second = self.stack.pop()
                first = self.stack.pop()
                self.stack.push(int(first >= second))
            elif instruction['type'] == LOAD: # The load memory instructions are used to load a number from a memory onto the stack.
                pass
            elif instruction['type'] == STORE:
                val = self.stack.pop()
                index = self.stack.pop()
                ea = index + int(instruction['offset'].split('=')[1])
                self.store['memAddr'][0]['data'][ea] = val
            elif instruction['type'] == SUB:
                second = self.stack.pop()
                first = self.stack.pop()
                self.stack.push(first - second)
            elif instruction['type'] == EQZ:
                self.stack.push(int(self.stack.pop() == 0))
            elif instruction['type'] == EQ:
                self.stack.push(int(self.stack.pop() == self.stack.pop()))
            elif instruction['type'] == OR:
                self.stack.push(int(self.stack.pop() or self.stack.pop()))
            elif instruction['type'] == LT_S:
                second = self.stack.pop()
                first = self.stack.pop()
                self.stack.push(int(first < second))
            elif instruction['type'] == DROP:
                self.stack.pop()
            elif instruction['type'] == RETURN:
                return                      
        
                






        def enterInstructionSequence(self, code, frame, type=-1):
        for i in range(len(code)):
            instruction = code[i]
            if instruction['type'] == BLOCK:
                # Enter instruction sequence
                self.stack.push(instruction)
                # Enter instruction sequence
                self.enterInstructionSequence(instruction["instructions"], frame,type=BLOCK)
            elif instruction['type'] == LOOP:
                # Push the label onto the stack
                self.stack.push(instruction)
                # Enter instruction sequence
                self.enterInstructionSequence(instruction["instructions"], frame,type=LOOP)
            elif instruction['type'] == LOCALGET:
                self.stack.push(frame.getLocal(int(instruction['operand'])))
            elif instruction['type'] == BR_IF:
                c = self.stack.pop()
                if c != 0:
                    for i in range(instruction['operand'] + 1):
                        # I.e., while there is a value on the stack
                        while not isinstance(self.stack.peek(), dict) and not isinstance(self.stack.peek(), Frame()):
                            self.stack.pop()
                        
                        # Pop the label from the stack
                        self.stack.pop()

                        # Jump to the continuation of L (for a block, this means breaking out of the current block)
                        if type==LOOP: 
                            return self.enterInstructionSequence(code, frame, type=type)
                        if type==BLOCK: 
                            return
                        
                else:
                    continue
            elif instruction['type'] == LOCALSET:
                val = self.stack.pop()
                frame.setLocalValue(val, int(instruction['operand']))
            elif instruction['type'] == LOCALTEE:
                frame.setLocalValue(self.stack.peek(), int(instruction['operand']))    
            elif instruction['type'] == CALL:
                # Get address of function in our store
                functionAddress = self.globalEnv.getIdentifierIndex("funcs", instruction['operand'])
                function = self.funcInstances[functionAddress]           
                self.callFunc(function)
            elif instruction['type'] == CONST:
                self.stack.push(int(instruction['operand']))
            elif instruction['type'] == ADD:
                self.stack.push(self.stack.pop() + self.stack.pop())
            elif instruction['type'] == GE_S:
                second = self.stack.pop()
                first = self.stack.pop()
                self.stack.push(int(first >= second))
            elif instruction['type'] == LOAD: # The load memory instructions are used to load a number from a memory onto the stack.
                pass
            elif instruction['type'] == STORE:
                val = self.stack.pop()
                index = self.stack.pop()
                ea = index + int(instruction['offset'].split('=')[1])
                self.store['memAddr'][0]['data'][ea] = val
            elif instruction['type'] == SUB:
                second = self.stack.pop()
                first = self.stack.pop()
                self.stack.push(first - second)
            elif instruction['type'] == EQZ:
                self.stack.push(int(self.stack.pop() == 0))
            elif instruction['type'] == EQ:
                self.stack.push(int(self.stack.pop() == self.stack.pop()))
            elif instruction['type'] == OR:
                self.stack.push(int(self.stack.pop() or self.stack.pop()))
            elif instruction['type'] == LT_S:
                second = self.stack.pop()
                first = self.stack.pop()
                self.stack.push(int(first < second))
            elif instruction['type'] == GE_S:
                second = self.stack.pop()
                first = self.stack.pop()
                self.stack.push(int(first >= second))
            elif instruction['type'] == DROP:
                self.stack.pop()
            elif instruction['type'] == RETURN:
                return                      
    
    """