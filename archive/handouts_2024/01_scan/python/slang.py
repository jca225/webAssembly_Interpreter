import sys
import slang_scanner


def getFromStdin(prompt):
    """Read a line from standard input (typically the keyboard).  If nothing is
    provided, return an empty string."""
    try:
        return input(prompt).rstrip()
    except EOFError:
        # we print a newline, because this is going to cause an exit, and it
        # will be a bit more graceful this way.
        print("")
        return ""


def getFile(filename):
    """Read a file and return its contents as a single string"""
    source_file = open(filename, "r")
    code = source_file.read()
    source_file.close()
    return code


def printHelp():
    """Print a help message"""
    print("slang -- An interpreter for a subset of Scheme, written in Python")
    print("  Usage: slang [mode] [filename]")
    print("    * If no filename is given, a REPL will read and evaluate one line of stdin at a time")
    print("    * If a filename is given, the entire file will be loaded and evaluated")
    print("  Modes:")
    print("    -help       Display this message and exit")
    print("    -scan       Scan slang code, output tokens as XML")
    print("    -parse      Parse from XML tokens, output an XML AST")
    print("    -interpret  Interpret from XML AST")
    print("    -full       Scan, parse, and interpret slang code")


def main(args):
    """Run the slang interpreter"""
    # Parse the command-line arguments.  Make sure exactly one valid mode is
    # given, and at most one filename
    filename, mode, numModes, numFiles = "", "", 0, 0
    for a in args:
        if a in ["-help", "-scan", "-parse", "-interpret", "-full"]:
            mode = a
            numModes += 1
        else:
            filename = a
            numFiles += 1
    if numModes != 1 or numFiles > 1 or mode == "-help":
        return printHelp()

    # Run the REPL loop, but only once if we have a valid filename
    while True:
        # Get some code
        codeToRun = ""
        if filename != "":
            codeToRun = getFile(filename)
        else:
            codeToRun = getFromStdin(":> ")
        if codeToRun == "":
            break

        # SCAN mode
        if mode == "-scan":
            tokens = slang_scanner.Scanner().scanTokens(codeToRun)
            while tokens.hasNext():
                print(slang_scanner.tokenToXml(tokens.nextToken()))
                tokens.popToken()
        # PARSE mode
        if mode == "-parse":
            print("-parse is not supported in p2.  Exiting...")
            break

        # INTERPRET mode
        if mode == "-interpret":
            print("-interpret is not supported in p2.  Exiting...")
            break

        # FULL mode
        if mode == "-full":
            print("-full is not supported in p2.  Exiting...")
            break

        if filename != "":
            break


# In python, this is how we get main() to run when we invoke this program via
# `python3 slang.py ...`
if __name__ == "__main__":
    main(sys.argv[1:])
