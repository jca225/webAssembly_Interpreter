from config import *

class TokenStream:
    def __init__(self, tokens):
        self.temp = tokens
        self.__tokens = tokens
        self.__next = 0

    def reset(self): self.__next = 0

    def nextToken(self):
        return None if not self.hasNext() else self.__tokens[self.__next]

    def nextNextToken(self):
        return None if not self.hasNextNext() else self.__tokens[self.__next + 1]

    def popToken(self): self.__next += 1

    def hasNext(self): return self.__next < len(self.__tokens)

    def hasNextNext(self): return (self.__next + 1) < len(self.__tokens)

class Token:
    """The Token class will be used for all token types in slang, since we
    don't need to subclass it for different literal types"""

    def __init__(self, tokenText, line, type, literal):
        """Construct a token from the text it corresponds to, the line/column
        where the text appears the token type, and an optional literal (an
        interpretation of that text as its real type)"""
        self.tokenText = tokenText
        self.line = line
        self.type = type
        self.literal = literal


class Scanner:

    def __init__(self):
        pass
    
    def advance(self, inc=1)  -> int:
        self.currentIndex += inc
        return self.currentIndex
    
    def abvance(self, inc=1)  -> int:
        self.currentIndex -= inc
        return self.currentIndex
    
    def isAtEnd(self)  -> bool:
        return self.currentIndex >= len(self.source)
    
    def current(self) -> str:
        return self.source[self.currentIndex]
    
    def next(self) -> str:
        return self.source[self.currentIndex+1]
    
    def hasNext(self, n=1) -> bool:
        return self.currentIndex+n < len(self.source)
    
    def incrementLine(self, inc=1) -> None:
        self.line += 1

    def isDigit(self) -> bool:
        return self.current() >= '0' and self.current() <= '9'
    
    def isAlpha(self) -> bool:
        return (self.current() >= 'a' and self.current() <= 'z') or (self.current() >= 'A' and self.current() <= 'Z')
    
    def isSpecialChar(self) -> bool:
        return self.current() in SPECIALCHARS
    
    def isIdChar(self) -> bool:
        return self.isAlpha() or self.isDigit() or self.isSpecialChar()
    
    def isHex(self) -> bool:
        return self.isDigit() or self.current() in HEXKVPAIRS
    

    def scanTokens(self, source: str) -> TokenStream:
        # Initialization of our variables
        self.startIndex = 0
        self.currentIndex = 0
        self.source = source
        self.line = 0
        self.tokens = []

        # NOTE: We base our grammar on the **longest match rule**, meaning
        # the next token always consists of the longest possible sequence of characters
        # that is recognized by the above lexical grammar.
        # All tokens must be separated by either parentheses, whitespace, or comments
        while not self.isAtEnd():
            if self.scanParentheses():
                continue
            if self.scanWhiteSpace():
                continue
            if self.scanIdentifier():
                continue
            if self.scanInteger():
                continue
            if self.scanString():
                continue
            if self.scanNumType():
                continue
            if self.scanFuncTypes():
                continue
            if self.scanModule():
                continue
            if self.scanExport():
                continue
            if self.scanImport():
                continue
            if self.scanInstructions():
                continue
        self.tokens.append(Token(tokenText='\0', line=self.line, type=EOF, literal='\0'))
        return TokenStream(self.tokens)
    
    def scanExport(self) -> bool:
        value = ""
        while self.current() not in TERMINALTOKENS:
            value += self.current()
            self.advance()
        if value == "export":
            self.tokens.append(Token(tokenText=value, line=self.line, type=EXPORT, literal=value))
            return True
        else:
            self.abvance(len(value))
            return False
        
    def scanImport(self) -> bool:
        value = ""
        while self.current() not in TERMINALTOKENS:
            value += self.current()
            self.advance()
        if value == "import":
            self.tokens.append(Token(tokenText=value, line=self.line, type=IMPORT, literal=value))
            return True
        else:
            self.abvance(len(value))
            return False
        
    def scanInstructions(self) -> bool:
        value = ""
        while self.current() not in TERMINALTOKENS:
            value += self.current()
            self.advance()
        if value in NUMTOKENS or value in VARTOKENS:
            self.tokens.append(Token(tokenText=value, line=self.line, type=INSTR, literal=value))
            return True
        else:
            self.abvance(len(value))
            return False
    def scanModule(self) -> bool:
        value = ""
        while self.current() not in TERMINALTOKENS:
            value += self.current()
            self.advance()
        if value == "module":
            self.tokens.append(Token(tokenText=value, line=self.line, type=MODULE, literal=value))
            return True
        else:
            self.abvance(len(value))
            return False
        
    def scanNumType(self) -> bool:
        value = ""
        while self.current() not in TERMINALTOKENS:
            value += self.current()
            self.advance()
        if value in NUMTYPES:
            self.tokens.append(Token(tokenText=value, line=self.line, type=NUMTYPE, literal=value))
            return True
        else:
            self.abvance(len(value))
            return False
        
    def scanFuncTypes(self) -> bool:
        value = ""
        while self.current() not in TERMINALTOKENS:
            value += self.current()
            self.advance()
        if value in FUNCTYPES:
            if value == 'func': tokenType = FUNC 
            elif value == 'param': tokenType = PARAM 
            elif value == 'local': tokenType = LOCAL
            elif value == 'result': tokenType = RESULT
            self.tokens.append(Token(tokenText=value, line=self.line, type=tokenType, literal=value))
            return True
        else:
            self.abvance(len(value))
            return False
    def scanParentheses(self) -> bool:
        # Check for '(', excluding '(;', which represents a comment
        if self.current() == '(':
            # If the next token exists and the next token does not imply there is a comment
            if self.hasNext():
                if self.next() != ';':
                    self.tokens.append(Token(tokenText='(', line=self.line, type=OPEN_PAREN, literal='('))
                    self.advance()
                    return True
                else:
                    return False
            else:
                return False
        elif self.current() == ')':
            self.tokens.append(Token(tokenText=')', line=self.line, type=CLOSE_PAREN, literal=')'))
            self.advance()
            return True
        return False
    
    def scanIdentifier(self) -> bool:
        identifier = ""
        if self.current() == '$':
            # As long as the characters are valid identifier tokens continue adding
            while self.isIdChar():
                identifier += self.current()
                self.advance()
            self.tokens.append(Token(tokenText=identifier, line=self.line, type=IDENTIFIER, literal=identifier))
            return True
        else:
            return False

    
    def scanWhiteSpace(self) -> bool:
        """Determines if there is currently a newline, carriage return, carriage return and newline, 
        or a comment"""
        isWhiteSpace = False
        while self.current() in WHITESPACETOKENS or self.scanComment():
            isWhiteSpace = True
            if self.current() == '\n':
                self.incrementLine()

            self.advance()

        return isWhiteSpace


    def scanComment(self) -> bool:
        """Determines if the next values to be scanned are comments. If so, then it scans them"""
        comment = ''
        # Make sure the next char exists
        if self.hasNext():
            # Line comment
            if self.current() == self.next() == ';':
                self.advance(2)
                while self.current() not in WHITESPACETOKENS and self.current() != '\0': # not a newline nor EOF
                    comment += self.current()
                    self.advance()
            # Block comment
            elif self.current() ==  '(' and self.next() == ';':
                self.advance(2)
                if self.hasNext():
                    while (self.current() != ';' and self.next() != ')') or (self.current() != '(' and self.next() != ';'):
                        self.comment += self.current()
                        self.advance()
                else:
                    raise Exception("Token Error: No end of comment on line: " + str(self.line) + ".")
            else:
                return False
        else:
            return False
        
        return True

    def scanInteger(self) -> bool:
        """Determines if the next values to be scanned are integers."""
        integer = ""
        # Minus sign
        if self.current() == '-':
            integer += '-'
            self.advance()
        # Plus sign
        elif self.current() == '+':    
            self.advance()

        # For scanning hex values, the next must exist
        if self.hasNext():
            # Hex convention '0x'
            if self.current() == '0' and self.next() == 'x':
                self.advance(2)

                # While there are valid characters to parse for the hex
                while self.isHex() or self.current() == '_':
                    integer += self.current()
                    self.advance()  
                self.tokens.append(Token(tokenText=integer, line=self.line, type=NUMERIC, literal=integer))
                return True      
        elif self.isDigit():
            while self.isDigit() or self.current() == '_':
                integer += self.current()
                self.advance()
            self.tokens.append(Token(tokenText=integer, line=self.line, type=NUMERIC, literal=int(integer)))
            return True
        
        return False
    

    def scanString(self) -> bool:
        """Determines if the next values to be scanned are strings"""
        string = ""
        # String token
        if self.current() == '"':
            self.advance()

            # While we do not reach a '"' token, or any other invalid token
            while self.current() != "\"" and self.current() >= '\u0020' and self.current() != '\u007F':
                if self.hasNext():
                    pass
                    '''
                    # Scan hexadecimal escape sequence
                    if self.current() == '\\' and self.next() == 'u':
                        self.advance(2)
                        # Opening curly bracket
                        if self.current() == '{':
                            self.advance()
                            # Where we will store our hex value
                            hexInteger = "\\u{"
                            # Must have closing curly bracket
                            while self.current() != '}':
                                
                                # Must have hex or '_' character
                                if self.isHex() or self.current() == '_':
                                    hexInteger += self.current()
                                else:
                                    raise Exception("Token Error: Expected hex value on line: " + str(self.line) + ".")
                                self.advance()
                            self.advance()
                            hexInteger += '}'
                            string += hexInteger
                        else:
                            raise Exception("Token Error: Expected hex value on line: " + str(self.line) + ".")
                    # If we have a hex value marked by '\nm' 
                    
                    elif self.current() == '\\':
                        hexIntegerValue = 0
                        hexInteger = self.current()
                        self.advance()
                        if self.hasNext():
                            if self.isHex(): 
                                hexIntegerValue += int(self.current()) * 16
                                hexInteger += self.current()
                                self.advance()
                            if self.isHex(): 
                                hexIntegerValue += int(self.current())
                                hexInteger += self.current()
                                self.advance()
                                continue
                        else:
                            raise Exception("Token Error: Expected hex value on line: " + str(self.line) + ".")
                        string += str(hexIntegerValue)
                        '''
                
                else:
                    raise Exception("Token Error: Expected ending quote \" value on line: " + str(self.line) + ".")
                string += self.current()
                self.advance()
            self.advance()
            self.tokens.append((Token(tokenText=string, line=self.line, type=STRING, literal=string))) 
            return True
        else:
            return False