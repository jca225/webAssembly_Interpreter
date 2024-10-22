import sys
import slang_scanner

codeToRun = "#t"
tokens = slang_scanner.Scanner().scanTokens(codeToRun)


while tokens.hasNext():
    print(slang_scanner.tokenToXml(tokens.nextToken()))
    tokens.popToken()