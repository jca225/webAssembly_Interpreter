# [mfs] The error messages in this file need some work.

# A poor-man's enum for the AST node types
AND, APPLY, BEGIN, BOOL, BUILTIN, CHAR, COND, CONS, DBL, DEFINE, IDENTIFIER, IF, INT, LAMBDADEF, LAMBDAVAL, OR, QUOTE, SET, STR, SYMBOL, TICK, VEC = range(
    0, 22)

# NB: The next block of functions is intentionally undocumented, because the
# documentation would be longer than the code.  What's happening here is that we
# are representing all AST node types as dictionaries.  Each node has a "type"
# field, which draws from the above enum, to determine the type.  All the other
# fields are defined on a per-type basis.
#
# There are two tricky cases:
# - A char is just a string with one element, because that's all Python allows
# - The cond node has a list of expr/list pairs, but the list is untyped


def AndNode(exprs): return {"type": AND, "exprs": exprs}
def ApplyNode(exprs): return {"type": APPLY, "exprs": exprs}
def BeginNode(exprs): return {"type": BEGIN, "exprs": exprs}
def BoolNode(val): return {"type": BOOL, "val": val}
def BuiltInNode(n, f): return {"type": BUILTIN, "name": n, "func": f}
def CharNode(val): return {"type": CHAR, "val": val}
def CondNode(conditions): return {"type": COND, "conditions": conditions}
def ConsNode(car, cdr): return {"type": CONS, "car": car, "cdr": cdr}
def DblNode(val): return {"type": DBL, "val": val}
def DefineNode(id, expr): return {"type": DEFINE, "id": id, "expr": expr}
def IdentifierNode(name): return {"type": IDENTIFIER, "name": name}
def IfNode(c, t, f): return {"type": IF, "cond": c, "true": t, "false": f}
def IntNode(val): return {"type": INT, "val": val}
def LambdaDefNode(f, b): return {"type": LAMBDADEF, "formals": f, "exprs": b}
def LambdaValNode(e, l): return {"type": LAMBDAVAL, "env": e, "lambda": l}
def OrNode(exprs): return {"type": OR, "exprs": exprs}
def QuoteNode(datum): return {"type": QUOTE, "datum": datum}
def SetNode(id, expr): return {"type": SET, "id": id, "expr": expr}
def StrNode(val): return {"type": STR, "val": val}
def SymbolNode(name): return {"type": SYMBOL, "name": name}
def TickNode(datum): return {"type": TICK, "datum": datum}
def VecNode(items): return {"type": VEC, "items": items}


def __unescape(s):
    """un-escape backslash, newline, tab, and apostrophe"""
    return s.replace("'", "\\'").replace("\n", "\\n").replace("\t", "\\t").replace("\\", "\\\\")


def XmlToAst(xml):
    """
    Given a string that is assumed to represent the output of astToXML,
    re-create the AST.

    Note that this is very brittle code.  It makes assumptions about things like
    newlines and whitespace that no good parser should ever assume.
    """
    res = []
    lines = xml.split("\n")
    next = 0

    def parseNext():
        """A helper function for parsing the next AST node"""
        nonlocal lines
        nonlocal next
        valStart = lines[next].find("val=")
        valEnd = len(lines[next]) - 3
        while next < len(lines) and lines[next] == "":
            next += 1
        if next >= len(lines):
            return None
        if lines[next].find("<Identifier") > -1:
            val = __unescape(lines[next][valStart + 5: valEnd - 1])
            next += 1
            return IdentifierNode(val)
        if lines[next].find("<Define") > -1:
            next += 1
            identifier = parseNext()
            expression = parseNext()
            next += 1
            return DefineNode(identifier, expression)
        if lines[next].find("<Bool") > -1:
            val = lines[next][valStart + 5: valEnd - 1]
            next += 1
            return BoolNode(val == "true")
        if lines[next].find("<Int") > -1:
            val = lines[next][valStart + 5: valEnd - 1]
            next += 1
            return IntNode(int(val))
        if lines[next].find("<Dbl") > -1:
            val = lines[next][valStart + 5: valEnd - 1]
            next += 1
            return DblNode(float(val))
        if lines[next].find("<Lambda") > -1:
            next += 2
            formals = []
            while lines[next].find("</Formals>") == -1:
                formals.append(parseNext())
            next += 2
            body = []
            while lines[next].find("</Expressions>") == -1:
                body.append(parseNext())
            next += 2
            return LambdaDefNode(formals, body)
        if lines[next].find("<If") > -1:
            next += 1
            cond = parseNext()
            true = parseNext()
            false = parseNext()
            next += 1
            return IfNode(cond, true, false)
        if lines[next].find("<Set") > -1:
            next += 1
            identifier = parseNext()
            expression = parseNext()
            next += 1
            return SetNode(identifier, expression)
        if lines[next].find("<And") > -1:
            next += 1
            exprs = []
            while lines[next].find("</And>") == -1:
                exprs.append(parseNext())
            next += 1
            return AndNode(exprs)
        if lines[next].find("<Or") > -1:
            next += 1
            exprs = []
            while lines[next].find("</Or>") == -1:
                exprs.append(parseNext())
            next += 1
            return OrNode(exprs)
        if lines[next].find("<Begin") > -1:
            next += 1
            exprs = []
            while lines[next].find("</Begin>") == -1:
                exprs.append(parseNext())
            next += 1
            return BeginNode(exprs)
        if lines[next].find("<Apply") > -1:
            next += 1
            exprs = []
            while lines[next].find("</Apply>") == -1:
                exprs.append(parseNext())
            next += 1
            return ApplyNode(exprs)
        if lines[next].find("<Cons") > -1:
            next += 1
            car = None
            cdr = None
            if lines[next].find("<Null />") == -1:
                car = parseNext()
            else:
                next += 1
            if lines[next].find("<Null />") == -1:
                cdr = parseNext()
            else:
                next += 1
            next += 1
            return ConsNode(car, cdr)
        if lines[next].find("<Vector") > -1:
            next += 1
            exprs = []
            while lines[next].find("</Vector>") == -1:
                exprs.append(parseNext())
            next += 1
            return VecNode(exprs)
        if lines[next].find("<Quote") > -1:
            next += 1
            datum = parseNext()
            next += 1
            return QuoteNode(datum)
        if lines[next].find("<Tick") > -1:
            next += 1
            datum = parseNext()
            next += 1
            return TickNode(datum)
        if lines[next].find("<Char") > -1:
            val = __unescape(lines[next][valStart + 5: valEnd - 1])
            next += 1
            literal = val.charAt(0)
            if val.equals("\\"):
                literal = '\\'
            elif val.equals("\\t"):
                literal = '\t'
            elif val.equals("\\n"):
                literal = '\n'
            elif val.equals("\\'"):
                literal = '\''
            return CharNode(literal)
        if lines[next].find("<Str") > -1:
            val = __unescape(lines[next][valStart + 5: valEnd - 1])
            next += 1
            return StrNode(val)
        if lines[next].find("<Cond") > -1:
            next += 1
            conditions = []
            while lines[next].find("<Condition>") > -1:
                next += 2
                test = parseNext()
                next += 2
                exprs = []
                while lines[next].find("</Actions>") == -1:
                    exprs.append(parseNext())
                next += 2
                conditions.append({"test": test, "exprs": exprs})
            next += 1
            return CondNode(conditions)
        raise Exception("Unrecognized XML tag: " + lines[next])

    # given our helper function, we can just iterate through the lines, passing
    # each to parseNext.
    while next < len(lines):
        tmp = parseNext()
        if tmp:
            res.append(tmp)
    return res

# [mfs] AstToScheme's indentation isn't great, and its pretty-printing really
#       stinks.  It's worth revisiting this: do we really need to print whole
#       ASTs as Scheme source, or just values?


def AstToScheme(expr, indentation, inList, empty):
    """Print an AST as nicely-formatted Scheme code"""
    def __indent():
        """Helper function for indentation"""
        res = ""
        for i in range(0, indentation):
            res += ""
        return res

    # for each of the AST Node types, print it as if it were scheme code
    #
    # [mfs] This code is very opinionated about how to format scheme code, and
    # it's a BAD opinion that nobody else in the world shares.
    if expr["type"] == IDENTIFIER:
        return __indent() + expr[1]
    if expr["type"] == DEFINE:
        res = __indent() + "(define\n"
        res += AstToScheme(expr[1], indentation+1, inList, empty) + "\n"
        res += AstToScheme(expr[2], indentation+1, inList, empty) + ")"
        return res
    if expr["type"] == BOOL:
        return __indent() + "#f" if not expr["val"] else "#t"
    if expr["type"] == INT:
        return __indent() + str(expr["val"])
    if expr["type"] == DBL:
        return __indent() + str(expr["val"])
    if expr["type"] == LAMBDADEF:
        res = __indent() + "(lambda ("
        indentation += 1
        for f in expr[1]:
            res += "\n" + AstToScheme(f, indentation+1, inList, empty)
        res += ")"
        for e in expr[2]:
            res += "\n" + AstToScheme(e, indentation+1, inList, empty)
        return res
    if expr["type"] == IF:
        res = __indent() + "(if\n"
        res += AstToScheme(expr[1], indentation+1, inList, empty) + "\n"
        res += AstToScheme(expr[2], indentation+1, inList, empty) + "\n"
        res += AstToScheme(expr[3], indentation+1, inList, empty) + ")"
        return res
    if expr["type"] == SET:
        res = __indent() + "(set!\n"
        res += AstToScheme(expr[1], indentation+1, inList, empty) + "\n"
        res += AstToScheme(expr[2], indentation+1, inList, empty) + ")"
        return res
    if expr["type"] == AND:
        res = __indent() + "(and"
        for e in expr[1]:
            res += "\n" + AstToScheme(e, indentation+1, inList, empty)
        return res + ")"
    if expr["type"] == OR:
        res = __indent() + "(or"
        for e in expr[1]:
            res += "\n" + AstToScheme(e, indentation+1, inList, empty)
        return res + ")"
    if expr["type"] == BEGIN:
        res = __indent() + "(begin"
        for e in expr[1]:
            res += "\n" + AstToScheme(e, indentation+1, inList, empty)
        return res + ")"
    if expr["type"] == APPLY:
        res = __indent()+"("
        for e in expr.expressions:
            res += "\n" + AstToScheme(e, indentation+1, inList, empty)
        return res + ")"
    # [mfs] Printing lists is something of a disaster right now...
    if expr["type"] == CONS:
        # [mfs] '(1 2 3) doesn't print nicely
        res = __indent()
        if expr == empty:
            res += "()"
            return res
        first = False
        if not inList:
            res += "("
            inList = True
            indentation += 1
            first = True
        res += "\n"
        car = expr["car"]
        cdr = expr["cdr"]
        if car == None:
            res += __indent() + "()"
        elif car["type"] == CONS:
            res += AstToScheme(car, indentation+1, False, empty)
        else:
            res += __indent() + AstToScheme(car, indentation+1, inList, empty)
        if cdr != empty:
            if cdr["type"] != CONS:
                res += ".\n" + __indent() + AstToScheme(cdr, indentation, inList, empty)
            else:
                res += __indent() + AstToScheme(cdr, indentation, inList, empty)
        if first:
            res += ")"
        return res
    if expr["type"] == VEC:
        res = __indent() + "#("
        for i in expr["items"]:
            res += "\n " + __indent() + AstToScheme(i, indentation+1, inList, empty)
        return res + ")"
    if expr["type"] == SYMBOL:
        return __indent() + expr["name"]
    if expr["type"] == QUOTE:
        return __indent() + "(quote\n" + AstToScheme(expr[1], indentation+1, inList, empty) + ")"
    if expr["type"] == TICK:
        return __indent()+"'\n" + AstToScheme(expr[1], indentation+1, inList, empty)
    if expr["type"] == CHAR:
        return __indent() + expr["val"]
    if expr["type"] == STR:
        return __indent() + expr["val"]
    if expr["type"] == BUILTIN:
        return __indent() + "Built-in Function ("+expr["name"]+")"
    if expr["type"] == LAMBDAVAL:
        return __indent() + "Lambda with " + str(len(expr["lambda"]["formals"])) + " args"
    if expr["type"] == COND:
        res = __indent() + "(cond"
        for c in expr[1]:
            res += "\n"+__indent() + "(\n"
            res += AstToScheme(c[0], indentation+1, inList, empty)
            for e in c[1]:
                res += "\n" + AstToScheme(e, indentation+1, inList, empty)
            res += ")"
        return res + ")"
