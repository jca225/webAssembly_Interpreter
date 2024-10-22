from settings import *

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

"""The following structs define the finite automata for our tokens"""
string = {
    "startState" : "\"",
    "acceptingState" : "\"",
    "transitionFn" : {"\\": "\""}
}

lineComment = {
    "startState" : ";;",
    "acceptingState" : "\n",
    "transitionFn" : None
}

blockComment = {
    "startState" : "(;",
    "acceptingState" : ";)",
    "transitionFn" : None
}

keyword = {
    "startState" : [chr(a) for a in range(97,123)],
    "acceptingState" : None,
    "transitionFn" : [chr(a) for a in range(97,123)] + [chr(a) for a in range(65,91)] + [str(a) for a in range(0,10)] + ['!', '#', '$', '%', '&', '`', '*', '-', '+', '.', '/', ':', '<', '=', '>', '?', '@', '\\', '^', '\'', '_', '|', '~']
}

integer = {
    "startState" : ['+', '-'] + [str(a) for a in range(0,10)],
    "acceptingState" : None,
    "transitionFn" : ['_'] + [str(a) for a in range(0,10)]
}

id = {
    "startState" : '$',
    "acceptingState" : None,
    "transitionFn" : ['!', '#', '$', '%', '&', '`', '*', '-', '+', '.', '/', ':', '<', '=', '>', '?', '@', '\\', '^', '\'', '_', '|', '~'] + [chr(a) for a in range(97,123)] + [chr(a) for a in range(65,91)] + [str(a) for a in range(0,10)]
}

class Scanner:

    def __init__(self):
        pass

    def advance(self, inc=1)  -> int:
        self.currentIndex += inc
        return self.currentIndex

    def isAtEnd(self)  -> bool:
        return self.currentIndex >= len(self.source)
    
    def current(self) -> str:
        return self.source[self.currentIndex]
    
    def next(self) -> str:
        return self.source[self.currentIndex+1]
    
    def scanTokens(self, source: str) -> TokenStream:
        """
        Source text is divided into a sequence of tokens based on the following grammar:
            token    --> keyword | uN | sN | fN | string | id | '(' | ')' | reserved
            keyword  --> ('a' | ... | 'z') idchar*
            reserved --> (idchar | string)+
        """
        # Initialization of our variables
        self.currentIndex = 0
        self.source = source
        self.line = 1
        self.tokens = []

        # While we are still parsing characters
        while not self.isAtEnd():
            # Block comment scan
            if self.current() == blockComment['startState'][0] and self.next() == blockComment['startState'][1]:
                self.advance(2)
                while self.current() != blockComment['acceptingState'][0] and self.next() != blockComment['acceptingState'][1]:
                    self.advance() 
                self.advance(2)

            # Line comment scan
            elif self.current() == lineComment['startState'][0] and self.next() == lineComment['startState'][1]:
                self.advance(2)
                while self.current() != lineComment['acceptingState']:
                    self.advance() 

            # String scan
            elif self.current() == string['startState']: # start state
                self.advance()
                startIndex = self.currentIndex
                while self.current() != string['acceptingState']:
                    if self.current() in string['transitionFn'] and self.next() != string['transitionFn'][self.current()]:
                        raise ValueError("Incorrect token.")
                    self.advance()
                self.advance()
                
                # Get the literal of the string that was parsed
                literal = self.source[startIndex:self.currentIndex-1]
                # Instantiate the token and append it to the list of tokens
                token = Token(literal, self.line, STR, literal)
                self.tokens.append(token)

            # Left parentheses scan
            elif self.current() == '(':
                self.advance()
                # Instantiate the token and append it to the list of tokens
                token = Token('(', self.line, LPAREN, '(')
                self.tokens.append(token)

            # Right parentheses scan
            elif self.current() == ')':
                self.advance()
                # Instantiate the token and append it to the list of tokens
                token = Token(')', self.line, RPAREN, ')')
                self.tokens.append(token)

            # Whitespace scan
            elif self.current() in ['\n', '\r', ' ']:
                if self.current() == '\n':
                    self.line += 1
                self.advance()

            # Keyword scan
            elif self.current() in keyword['startState']:
                startIndex = self.currentIndex
                self.advance()
                # While the tokens we are parsing are valid for the keyword
                while self.current() in keyword['transitionFn']:
                    self.advance()
                
                # parse the literal
                literal = self.source[startIndex:self.currentIndex]
                type = None
                comparisonLiteral = literal

                # Check if there is a '.'
                if comparisonLiteral.split(".")[0] != literal:
                    # If there is, split the string into two
                    comparisonLiteral = comparisonLiteral.split(".")
                    if comparisonLiteral[0] == 'global':
                        if comparisonLiteral[1] == 'get':
                            type = GLOBALGET
                        if comparisonLiteral[1] == 'set':
                            type = GLOBALSET
                        if comparisonLiteral[1] == 'tee':
                            type = GLOBALTEE
                    elif comparisonLiteral[0] == 'local':
                        if comparisonLiteral[1] == 'get':
                            type = LOCALGET
                        if comparisonLiteral[1] == 'set':
                            type = LOCALSET
                        if comparisonLiteral[1] == 'tee':
                            type = LOCALTEE
                    else:
                        comparisonLiteral = comparisonLiteral[1]
                        for i in range(len(KVPAIRS)):
                    
                            # If a keyword is abstract, continue
                            if KVPAIRS[i] == None:
                                continue
                                
                            # If the keyword is found, assign it an index (type)
                            if comparisonLiteral == KVPAIRS[i]:
                                type = i
                                break
                            else:
                                continue
                    token = Token(literal, self.line, type, literal)
                    self.tokens.append(token) 
                    continue  
                # The same logic as before, only with '='
                elif literal.split("=")[0] != literal:
                    comparisonLiteral = comparisonLiteral.split("=")[0]
                    # Loop through our saved keywords
                for i in range(len(KVPAIRS)):
                    
                    # If a keyword is abstract, continue
                    if KVPAIRS[i] == None:
                        continue
                        
                    # If the keyword is found, assign it an index (type)
                    if comparisonLiteral == KVPAIRS[i]:
                        type = i
                        break
                    else:
                        continue
                        
                # Instantiate the token and append it to the list of tokens
                token = Token(literal, self.line, type, literal)
                self.tokens.append(token)   

            # Integer scan
            elif self.current() in integer['startState']:
                startIndex = self.currentIndex
                self.advance()
                while self.current() in integer['transitionFn']:
                    self.advance()
                
                literal = int(self.source[startIndex:self.currentIndex])
                type = INT
                token = Token(literal, self.line, type, literal)
                self.tokens.append(token)   

            # ID scan
            elif self.current() == id['startState']:
                startIndex = self.currentIndex
                self.advance()
                while self.current() in id['transitionFn']:
                    self.advance()

                literal = self.source[startIndex:self.currentIndex]
                type = ID
                token = Token(literal, self.line, type, literal)
                self.tokens.append(token)   

            else:
                raise ValueError("Error scanning tokens.")
        
        type = EOF
        self.tokens.append(Token('\0', self.line, type, '\0'))    
        return TokenStream(self.tokens)
    
