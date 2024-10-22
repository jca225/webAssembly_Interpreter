from settings import *
from env import *

class Parser:
    """The parser class is responsible for parsing a stream of tokens to produce
    an AST"""

    def __init__(self):
        """Construct a parser"""
        self.tokens = None
        self.identifierContext = Env()
        self.typesToInsert = []
        self.labelIndex = 0
    

    def parse(self, tokens):
        """Main module for our parser. The basic building block is a module"""
        self.tokens=tokens
        moduleId = None
        moduleFields = None
        while not self.checkKeyword(EOF): # we check to make sure the current token we are on is not EOF  
            # Parse a module
            if self.checkOpenParentheses() and self.checkKeyword(MODULE):
                # Optional identifier
                if self.tokens.nextToken().type == ID:
                    moduleId = self.tokens.nextToken().literal
                # the value is of type module field
                moduleFields = self.parseModuleField()
            # Assert closing parentheses
            self.checkClosingParentheses()
        return {"id": moduleId, "fields": moduleFields, "env": self.identifierContext}
       
    def parseModuleField(self):
        """Parse a module field"""
        moduleFields = []
        # Check for opening parentheses
        while self.checkOpenParentheses():
            moduleField = {}
            # Check if we are parsing a function
            if self.checkKeyword(FUNC):
                moduleField = self.parseFunc() #TODO: We end instruction parsing based on ending parnetheses. fix this
            # Check if we are parsing an export
            elif self.checkKeyword(EXPORT):
                moduleField = self.parseExport()
            # Check if we are parsing a type
            elif self.checkKeyword(TYPE):
                moduleField = self.parseType()
            # Check if we are parsing a table
            elif self.checkKeyword(TABLE):
                moduleField = self.parseTable()
            # Check if we are parsing memory
            elif self.checkKeyword(MEMORY):
                moduleField = self.parseMemory()
            # Check if we are parsing a global
            elif self.checkKeyword(GLOBAL):
                moduleField = self.parseGlobal()
            elif self.checkKeyword(IMPORT):
                moduleField = self.parseImport()
            # Assert closing parentheses
            self.checkClosingParentheses()
            moduleFields.append(moduleField)
        return moduleFields


    def parseFunc(self):
        # Add id to integer index mapping to the identifier context
        id = self.parseOptionalIdentifier('funcs') 
        # Create type index and frame
        typeidx, frame = self.parseTypeUse()
        self.parseLocals(frame)
        instructions = []
        while not self.checkClosingParentheses():
            instructions.append(self.parseInstruction())
        # Reset label index
        self.labelIndex = 0
        return {'type': FUNC, "id": id, "typeidx": typeidx, "frame": frame, "instr": instructions}

    def parseOptionalIdentifier(self, type):
        """Parse identifier and store it in type's identifier space"""
        if self.tokens.nextToken().type == ID:
            identifier = self.tokens.nextToken().literal
            self.tokens.popToken()
            return self.identifierContext.addIdentifierIndex(type, identifier)
        return self.identifierContext.addIdentifierIndex(type, None)

    def parseIdx(self, type):
        """Inverse of `parseOptionalIdentifier()` (i.e., get instead of set). 
           return the index itself or the index associated with the identifier"""
        if self.tokens.nextToken().type == ID:
            identifier = self.tokens.nextToken().literal
            self.tokens.popToken()
            return self.identifierContext.getIdentifierIndex(type, identifier)
        identifier = self.tokens.nextToken().literal
        self.tokens.popToken()
        return self.identifierContext.getIdentifierIndex(type, identifier)

    def parseType(self):
        """Takes as input type definition, adds the type to the identifier context and returns the node"""
        # Parse optional identifier into the environment
        id = self.parseOptionalIdentifier("types")
        # Pop '(' and 'func' tokens
        self.tokens.popToken()
        self.tokens.popToken()
        # Parse functype
        frame = self.parseFuncType()
        # Get closing parentheses for functype
        self.checkClosingParentheses()
        return {"type": TYPE, "id": id, "frame": frame}

        
    def parseFuncType(self):
        frame = Frame()
        self.parseParams(frame)
        self.parseResults(frame)
        return frame

    def parseTypeUse(self):
        # Assert opening parentheses
        self.checkOpenParentheses()
        # Create new call frame
        frame = Frame()
        # parse Typeuse
        if self.checkKeyword(TYPE):
            # Add mapping from the id or the integer index to the functional type in the identifier context
            parsedTypeIdx = self.parseIdx('type')
            self.checkClosingParentheses()

            self.parseParams(frame)
            self.parseResults(frame)
            return parsedTypeIdx, frame
        # Parse the corresponding abbreviation of the typeuse
        else:
            self.parseParams(frame)
            self.parseResults(frame)
            # If a type index does not exist, then it is inserted based on the global scope
            typeidx = self.identifierContext.createIdentifierIndex("types", None)
            # If we are not parsing a block, then add the implicit type to the end of the module
            #if not parseBlock: self.typesToInsert.append({"type": TYPE, "id": typeidx, "params": env.getParams(), "results": env.getResults()})
            return typeidx, frame

    def parseParams(self, frame):
        if self.checkOpenParentheses() and self.checkKeyword(PARAM):
            # Abbreviation mechanism. This mechanism only works for parameters with no ids
            if self.tokens.nextToken().type in [I32, I64, F32, F64] and self.tokens.nextToken().type in [I32, I64, F32, F64]:
                while not self.checkClosingParentheses():
                    # Pop token
                    self.tokens.popToken()
                    # Add anonymous parameters of certain types to the local environment's locals   
                    identifier = None
                    type = self.tokens.nextToken().type
                    frame.setLocal({"id": identifier, "type": type})
                    frame.addArg({"id": identifier, "type": type})

            # Regular parsing mechanism (i.e., no abbreviations)
            else:
                while True:
                    if self.tokens.nextToken().type == ID:
                        identifier = self.tokens.nextToken().literal
                        self.tokens.popToken()
                        type = self.tokens.nextToken().type
                        frame.setLocal({"id": identifier, "type": type})
                        frame.addArg({"id": identifier, "type": type})
                    else:
                        identifier = None
                        type = self.tokens.nextToken().type
                        # Pop token
                        self.tokens.popToken()
                        frame.setLocal({"id": identifier, "type": type})
                        frame.addArg({"id": identifier, "type": type})
                    if not self.checkParenthesesKeyword(PARAM):
                        break
      
    def parseLocals(self, frame):
        if self.checkOpenParentheses() and self.checkKeyword(LOCAL):
            # Abbreviation mechanism. This mechanism only works for parameters with no ids
            if self.tokens.nextToken().type in [I32, I64, F32, F64] and self.tokens.nextToken().type in [I32, I64, F32, F64]:
                while not self.checkClosingParentheses():
                    # Pop token
                    self.tokens.popToken()
                    identifier = None
                    type = self.tokens.nextToken().type
                    frame.setLocal({"id": identifier, "type": type})

            # Regular parsing mechanism (i.e., no abbreviations)
            else:
                while True:
                    if self.tokens.nextToken().type == ID:
                        identifier = self.tokens.nextToken().literal
                        self.tokens.popToken()
                        type = self.tokens.nextToken().type
                        frame.setLocal({"id": identifier, "type": type})
                    else:
                        identifier = None
                        type = self.tokens.nextToken().type
                        # Pop token
                        self.tokens.popToken()
                        frame.setLocal({"id": identifier, "type": type})
                    if not self.checkParenthesesKeyword(PARAM):
                        break

    def parseResults(self, frame):
        if self.checkOpenParentheses() and self.checkKeyword(RESULT):
            # Abbreviation mechanism. This mechanism only works for parameters with no ids
            if self.tokens.nextToken().type in [I32, I64, F32, F64] and self.tokens.nextToken().type in [I32, I64, F32, F64]:
                while not self.checkClosingParentheses():
                    valtype = self.tokens.nextToken().type
                    self.tokens.popToken()
                    frame.addReturn(valtype)
        
    def parseInstruction(self):
        block = self.checkKeyword(BLOCK)
        loop = self.checkKeyword(LOOP)
        if block or loop:
            # Add optional label to the local environment 
            # label = self.parseOptionalIdentifier("labels")
            # While the instruction sequence does not see the 'end' keyword, parse instructions
            instructions = []
            while not self.checkKeyword(END):
                instructions.append(self.parseInstruction())

            if block: return {"type": BLOCK, "instructions": instructions, "index": 1}
            if loop: return {"type": LOOP, "instructions": instructions, "index": 1}
        elif self.checkKeyword(IF):
            pass
        else:
            instructionType = self.tokens.nextToken().type
            self.tokens.popToken()
            if self.tokens.nextToken().type == ID or self.tokens.nextToken().type == INT:
                op = self.tokens.nextToken().literal
                self.tokens.popToken()
                return {"type": instructionType, "operand": op}
            else:
                return {"type": instructionType, "operand": None}
        

    def parseImport(self):
        module = self.tokens.nextToken().literal
        self.tokens.popToken()
        name = self.tokens.nextToken().literal
        self.tokens.popToken()
        importDesc = self.parseImportDesc() 
        return {"type": IMPORT, "module": module, "name": name, "importDesc": importDesc}
    
    def parseImportDesc(self):
        if self.checkOpenParentheses():
            if self.checkKeyword(FUNC):
                id = self.parseOptionalIdentifier("funcs")
                idx,env = self.parseTypeUse()
                self.checkClosingParentheses()
                return {"type": TYPEUSE, "id": id, "env": env}

            elif self.checkKeyword(TABLE):
                id = self.parseOptionalIdentifier("tables")
                tabletype = self.parseTableType()
                self.checkClosingParentheses()

            elif self.checkKeyword(MEMORY):
                id = self.parseOptionalIdentifier("mems")
                memtype = self.parseLimits()
                self.checkClosingParentheses()
                return {"type": MEMORY, "id": id, "valtype": memtype}
                
            elif self.checkKeyword(GLOBAL):
                id = self.parseOptionalIdentifier("globals")
                globalType = self.parseGlobalType()
                self.checkClosingParentheses()
                return {"type": GLOBAL, "id": id, "valtype": globalType}
  
    def parseExport(self):
        name = self.tokens.nextToken().literal
        self.tokens.popToken()
        idx = self.parseExportDesc() 
        return {"type": EXPORT, "name": name, "id": idx}
    
    def parseExportDesc(self):
        self.checkOpenParentheses()
        if self.checkKeyword(FUNC):
            idx = self.parseIdx("funcs")
            return idx
    def parseLimits(self):
        min = max = 0
        if self.tokens.nextToken().type == INT:
            min = self.tokens.nextToken().literal
            self.tokens.popToken()
        if self.tokens.nextToken().type == INT:
            max = self.tokens.nextToken().literal
            self.tokens.popToken()
            return {"type": LIMITS, "min": min, "max": max}
        else:
            return {"type": LIMITS, "min": min}
        
    def checkKeyword(self, type):
        if self.tokens.nextToken().type == type:
            self.tokens.popToken()
            return True
        return False
    
    def checkOpenParentheses(self):
        if self.tokens.nextToken().type == LPAREN:
            self.tokens.popToken()
            return True
        return False
    
    def checkClosingParentheses(self):
        if self.tokens.nextToken().type == RPAREN:
            self.tokens.popToken()
            return True
        return False