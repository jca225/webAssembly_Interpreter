# [CSE 262] This file is a minimal skeleton for a Scheme scanner in Python.  It
# provides a transliteration of the TokenStream class, and the shell of a
# Scanner class.  Please see the README.md file for more discussion.

class TokenStream:
    def __init__(self, tokens):
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


class Scanner:

    keywords = {
        "and": "AND",
        "lambda": "LAMBDA",
        "or": "OR",
        "if": "IF",
        "set!": "SET",
        "begin": "BEGIN",
        "cond": "COND",
        "quote": "QUOTE",

    }

    symbols = ['!', '&', '*', '/', ':', '<', '=', '>', '?', '~', '_', '^', '%', '$']
    source = ""
    start = current = 0 # both a member of natural numbers {0,1,2,...,n-1}, where n is the length of source
    specialStringChars = ['"', '\\', 't', 'n']
    changeState = [' ', '\t', '\n', '\r', '(', ')', ';', '\0']
    parenthChars = ['(', ')']
    tokens = []
    line = 0
    def __init__(self):
        pass

    def scanTokens(self, source):
        self.source = source
        while not self.isAtEnd():
            self.start = self.current
            self.scanTokensHelper()
        print(self.tokens)
        return TokenStream(self.tokens)

    def scanTokensHelper(self):

        if self.cleanBreak():
            if self.currentChar() in self.parenthChars:
                self.tokens.append(self.currentChar())
            elif self.currentChar() == '\n':
                self.line+=1
            elif self.isComment():
                self.comment()
            self.advance()

        elif self.currentChar() == '"': # handle strings
            self.string()
        elif self.isAlpha() or self.isSymbol(): # identifier
            self.identifier()

        elif self.isPM():
            self.advance()
            # only a digit can follow a '+' or '-' symbol
            if (self.isDigit()):
                self.isIntDbl()
            else:
                self.tokens.append("Parsing error at line " + str(self.line))
        elif (self.isDigit()):
            self.isIntDbl()
        elif self.currentChar() == '#':
            self.isVecCharBool()
        else: # any other character that is not in our finite state machine is considered an error
            self.tokens.append("Parsing error at line " + str(self.line))
            self.advance()

    
    def cleanBreak(self):
        return self.current >= len(self.source) or self.currentChar() in self.changeState
    
    def isAtEnd(self):
        return self.current >= len(self.source)
    
    def isPM(self):
        return self.currentChar() in ['+','-']
    
    def currentChar(self):
        return self.source[self.current]
    
    def isComment(self):
        return self.currentChar() == ';'
    
    def advance(self):
        self.current += 1
    
    def isDigit(self):
        return self.currentChar() >= '0' and self.currentChar() <= '9'
    
    def isAlpha(self):
        return (self.currentChar() >= 'a' and self.currentChar() <= 'z') or (self.currentChar() >= 'A' and self.currentChar() <= 'Z')
    
    def isSymbol(self):
        return (self.currentChar() in self.symbols)
    
    def isIdentifier(self):
        ops = ['.', '+', '-']
        return self.isAlpha() or self.isDigit() or self.isSymbol() or (self.currentChar() in ops)
        
    def isIntDbl(self):
        # parse digit
        while not self.cleanBreak() and self.isDigit():
            self.advance()

        # At the end and digits captured
        if self.cleanBreak():
            self.tokens.append(self.source[self.start:self.current]) 
            self.advance()
            return
        
        elif self.currentChar() == '.': # double (?)
            self.advance()
            if self.cleanBreak() or not self.isDigit(): # i.e., no digits after '.'
                self.tokens.append("Double parsing error at line: " + str(self.line))
                return
            
            # while there are digits and we are not at the end
            while not self.cleanBreak() and self.isDigit():
                self.advance()

            self.tokens.append(self.source[self.start:self.current]) 
            return
        
        # Stop due to non-integer value
        else:
            self.tokens.append("Unexpected character at line: " + str(self.line))
            
    def string(self):
        self.advance()
        # Note our while loop conditions is mutually exclusive; we cannot be both at the end and have a valid character
        while (not self.isAtEnd() and self.currentChar() != '"'):
            if (self.currentChar() == '\\'):
                self.advance()
                while (not self.isAtEnd() and not self.currentChar() in self.specialStringChars):
                    self.advance()
                else:
                    self.advance()
            else:
                self.advance()
        # got to the end before '"'
        if (self.isAtEnd()):
            self.tokens.append("String parsing error at line: " + str(self.line))
            return
        
        self.tokens.append(self.source[self.start+1:self.current])
        self.advance()

    def comment(self):
        self.advance()
        while not self.isAtEnd() and self.currentChar() != '\0'and self.currentChar() != '\n':
            self.advance()
        self.tokens.append("\0")
    
    def identifier(self):
        while (not self.cleanBreak() and self.isIdentifier()):
            self.advance()
        
        # substring classified as identifier
        text = self.source[self.start:self.current]

        # keywords take precedence over identifiers; Note also keywords are a subset of identifiers
        if text in self.keywords:
            self.tokens.append(self.keywords[text])
            return
        self.tokens.append(text)
        return

    def isVecCharBool(self):
        self.advance()

        # vector
        if self.currentChar() == '(':
            self.tokens.append("VEC")
            return
        
        # prechar
        elif self.currentChar() == '\\':
            self.advance()
            if self.currentChar() not in [' ', '\t', '\n', '\r', '\0']:
                self.tokens.append(self.currentChar())
                self.advance()
                return
        # char
        elif self.currentChar() == '\n' or self.currentChar() == ' ' or self.currentChar() == '\t':
            self.tokens.append(self.currentChar())
            self.advance()
            return
        elif self.currentChar() == 't' or self.currentChar() == 'f':
            self.tokens.append(self.currentChar())
            self.advance()
            return


def tokenToXml(token):
    return ""
