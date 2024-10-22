
import sys
import slang_parser
import slang_evaluator
import slang_env




def getFile(filename):
    """Read a file and return its contents as a single string"""
    source_file = open(filename, "r")
    code = source_file.read()
    source_file.close()
    return code

filename = "/Users/johncabrahams/Desktop/Projects/Research Project/handouts_2024/02_parse/tests/parse/pass_quote_4.scm.scan"
codeToRun = getFile(filename)

defaultEnv = slang_env.makeDefaultEnv()

expressions = slang_parser.XmlToAst(codeToRun)
for expr in expressions:
    result = slang_evaluator.evaluate(expr, defaultEnv)
    if result != None:
        print(";" + slang_evaluator.AstToScheme(result, 0, False, defaultEnv.empty))