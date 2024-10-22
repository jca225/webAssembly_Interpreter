# A poor-man's enum: each of our token types is just a number
ABBREV, AND, BEGIN, BOOL, CHAR, COND, DBL, DEFINE, EOFTOKEN, IDENTIFIER, IF, INT, LAMBDA, LEFT_PAREN, OR, QUOTE, RIGHT_PAREN, SET, STR, VECTOR = range(
    0, 20)


class Token:
    """The Token class will be used for all token types in slang, since we
    don't need to subclass it for different literal types"""

    def __init__(self, tokenText, line, col, type, literal):
        """Construct a token from the text it corresponds to, the line/column
        where the text appears the token type, and an optional literal (an
        interpretation of that text as its real type)"""
        self.tokenText = tokenText
        self.line = line
        self.col = col
        self.type = type
        self.literal = literal


class TokenStream:
    """TokenStream is a transliteration of the Java TokenStream.  It's just a
    sort of iterator-with-lookahead wrapper around a list of tokens"""

    def __init__(self, tokens):
        """Construct a TokenStream by setting the list to `tokens` and resetting
        the iterator position to 0"""
        self.__tokens = tokens
        self.__next = 0

    def reset(self):
        """Reset the token stream iterator to the first token"""
        self.__next = 0

    def nextToken(self):
        """Return (by peeking) the next token in the stream, if it exists"""
        return None if not self.hasNext() else self.__tokens[self.__next]

    def nextNextToken(self):
        """Return (by peeking) the token that is two positions forward in the
        stream, if it exists"""
        return None if not self.hasNextNext() else self.__tokens[self.__next + 1]

    def popToken(self):
        """Advance the token stream by one"""
        self.__next += 1

    def hasNext(self):
        """Report whether a peek forward will find a token or not"""
        return self.__next < len(self.__tokens)

    def hasNextNext(self):
        """Report whether a peek forward by two positions will find a token or
        not"""
        return (self.__next + 1) < len(self.__tokens)


def XmlToTokens(xml: str):
    """
    Given a string that is assumed to represent the output of tokenToXML,
    re-create the token stream

    Note that this is very brittle code.  It makes assumptions about things like
    newlines and whitespace that no good parser should ever assume.
    """
    def unescape(s):
        """un-escape backslash, newline, tab, and apostrophe"""
        return s.replace("\\'", "'").replace("\\n", "\n").replace("\\t", "\t").replace("\\\\", "\\")

    # we're just going to split the string into its lines, then look for
    # attributes and closing tags and use them to get all the parts
    res = []
    for token in xml.split("\n"):
        if token == "":
            continue
        firstSpace = int(token.find(" "))
        type = token[1: firstSpace]
        if type == "EofToken":
            res.append(Token("", 0, 0, EOFTOKEN, None))
            continue

        lineStart = token.find("line=")
        lineEnd = token.find(" ", lineStart + 2)
        colStart = token.find("col=")
        colEnd = token.find(" ", colStart + 2)
        line = int(token[lineStart + 5: lineEnd])
        col = int(token[colStart + 4: colEnd])

        valStart, valEnd = token.find("val="), len(token) - 3

        # so many of the tokens are done in the same way, so we can create a
        # hash of their name/type pairs, and use them to eliminate most of the
        # cases
        basicTokens = {"AbbrevToken": ("'", ABBREV), "AndToken": ("and", AND), "BeginToken": ("begin", BEGIN), "CondToken": ("cond", COND), "DefineToken": ("define", DEFINE), "IfToken": ("if", IF), "LambdaToken": (
            "lambda", LAMBDA), "LParenToken": ("(", LEFT_PAREN), "OrToken": ("or", OR), "QuoteToken": ("quote", QUOTE), "RParenToken": (")", RIGHT_PAREN), "SetToken": ("set!", SET), "VectorToken": ("#(", VECTOR)}
        if type in basicTokens.keys():
            val = basicTokens[type]
            res.append(Token(val[0], line, col, val[1], None))
        # All that remain are identifiers and datum tokens:
        elif type == "BoolToken":
            if token[valStart + 5: valEnd - 1] == "true":
                res.append(Token("#t", line, col, BOOL, True))
            else:
                res.append(Token("#f", line, col, BOOL, False))
        elif type == "CharToken":
            val = unescape(token[valStart + 5: valEnd - 1])
            literal = val[0]
            if val == "\\":
                literal, val = '\\',  "#\\\\"
            elif val == "\\t":
                literal, val = '\t', "#\\tab"
            elif val == "\\n":
                literal, val = '\n', "#\\newline"
            elif val == "\\'":
                literal, val = '\'', "#\\'"
            elif val == " ":
                val = "#\\space"
            else:
                val = "#\\" + val
            res.append(Token(val, line, col, CHAR, literal))
        elif type == "DblToken":
            val = token[valStart + 5: valEnd - 1]
            res.append(Token(val, line, col, DBL, float(val)))
        elif type == "IdentifierToken":
            res.append(
                Token(unescape(token[valStart + 5: valEnd - 1]), line, col, IDENTIFIER, None))
        elif type == "IntToken":
            val = token[valStart + 5: valEnd - 1]
            res.append(Token(val, line, col, INT, int(val)))
        elif type == "StrToken":
            val = unescape(token[valStart + 5: valEnd - 1])
            res.append(Token(val, line, col, STR, val))
        else:
            raise Exception("Unrecognized type: " + type)
    return TokenStream(res)
