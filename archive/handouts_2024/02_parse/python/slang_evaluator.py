import slang_parser

ABBREV, AND, BEGIN, BOOL, CHAR, COND, DBL, DEFINE, EOFTOKEN, IDENTIFIER, IF, INT, LAMBDA, LEFT_PAREN, OR, QUOTE, RIGHT_PAREN, SET, STR, VECTOR, DEF, BODY, FORMALS, LIST, APPLIC = range(
    0, 25)
TYPE = 'type'
VALUE = 'value'

#import slang_stdlib


class Env:
    """An environment/scope in which variables are defined"""

    def __init__(self, outer, poundF, poundT, empty):
        """Construct an environment.  We need a single global value for false,
        for true, and for empty. We optionally have a link to an enclosing
        scope"""
        self.outer = outer
        self.map = {}
        self.poundF = poundF
        self.poundT = poundT
        self.empty = empty

    def put(self, key, val):
        """Unconditionally put a key into this environment"""
        self.map[key] = val

    def get(self, key):
        """Look up the value for a given key; recurse to outer environments as
        needed.  Throw an exception on failure."""
        return self.map[key] if key in self.map.keys() else self.outer.get(key)

    def update(self, key, val):
        """Update a key's value **in the scope where it is defined**"""
        if self.map.get(key) != None:
            self.map[key] = val
        else:
            self.outer.update(key, val)


def makeDefaultEnv():
    """Create a default environment by mapping all the built-in names (true,
    false, empty list, and the built-in functions)"""
    poundF = {TYPE: BOOL, VALUE: False}#slang_parser.BoolNode(False)
    poundT = {TYPE: BOOL, VALUE: True} #slang_parser.BoolNode(True)
    empty = []# slang_parser.ConsNode(None, None)
    e = Env(None, poundF, poundT, empty)
    # [mfs] Still a lot to do here:
    #slang_stdlib.addMathFuncs(e)
    #slang_stdlib.addListFuncs(e)
    #slang_stdlib.addStringFuncs(e)
    #slang_stdlib.addVectorFuncs(e)
    return e


def evaluate(expr, env):
    
    """Evaluate is responsible for visiting an expression and producing a
    value"""
    if expr[TYPE] == DEF:
        key = expr[VALUE][IDENTIFIER]
        val = evaluate_expr(expr[VALUE][VALUE], env)
        env.put(key, val)
        return val
    else:
        return evaluate_expr(expr, env)

def evaluate_expr(expr, env):
    
    """Evaluate is responsible for visiting an expression and producing a
    value"""

    absorbing_states = [BOOL, INT, DBL, STR, CHAR]

    if expr[TYPE] == QUOTE:
        return evaluate_datum(expr[VALUE], env)

    elif expr[TYPE] == IF:
        condition = expr[VALUE][0]
        if_expr = evaluate_expr(expr[VALUE][1], env)
        else_expr = evaluate_expr(expr[VALUE][2], env)
        if condition:
            return if_expr
        else:
            return else_expr
        
    elif expr[TYPE] == AND:
        ret_expr = evaluate_expr(expr[VALUE][0], env)
        for i in range(1, len(expr[VALUE])):
            ret_expr = ret_expr and evaluate_expr(expr[VALUE][i])
        return ret_expr
    
    elif expr[TYPE] == OR:
        ret_expr = evaluate_expr(expr[VALUE][0], env)
        for i in range(1, len(expr[VALUE])):
            ret_expr = ret_expr or evaluate_expr(expr[VALUE][i])
        return ret_expr
    
    elif expr[TYPE] == SET:
        val = evaluate_expr(expr[VALUE][VALUE])
        env.update(expr[VALUE][IDENTIFIER], val)
        return val
    
    elif expr[TYPE] == COND:
        '''
        cond works by searching through its arguments in order. 
        It finds the first argument whose first element returns #t when evaluated, 
        and then evaluates and returns the second element of that argument. 
        It does not go on to evaluate the rest of its arguments.
        '''
        for cond_expr in expr[VALUE]:
            evaluated_cond_expr = evaluate_condition(cond_expr, env)
            if evaluated_cond_expr != None:
                return evaluated_cond_expr
            
    elif expr[TYPE] in absorbing_states:
        return expr[VALUE]
    


def evaluate_condition(cond_expr, env):
    expr_list = cond_expr[VALUE]
    i = 0
    for i in range(len(expr_list)):
        if evaluate_expr(expr_list[i]) == env.poundT:
            break
    return evaluate_expr(expr_list[i+1])


def evaluate_datum(expr, env):
    absorbing_states = [BOOL, INT, DBL, STR, CHAR]
    # absorbing states return the value themselves (aka)
    if expr[TYPE] in absorbing_states:
        return expr[VALUE]
    # identifier state returns the constant/value associated with the identifier
    elif expr[TYPE] == IDENTIFIER:
        return env.get(expr[VALUE])
    elif expr[TYPE] == LIST:
        return evaluate_list(expr[VALUE], env)
    elif expr[TYPE] == VECTOR:
        return evaluate_vector(expr[VALUE], env)

'''
<expression --> LPAREN QUOTE <datum> RPAREN
              | LPAREN LAMBDA <formals> <body> RPAREN
              | LPAREN IF <expression> <expression> <expression> RPAREN
              | LPAREN SET IDENTIFIER <expression> RPAREN
              | LPAREN AND <expression>+ RPAREN
              | LPAREN OR <expression>+ RPAREN
              | LPAREN BEGIN <expression>+ RPAREN
              | LPAREN COND <condition>+ RPAREN
              | ABBREV <datum>
              | <constant>
              | IDENTIFIER
              | <application>
'''  

def evaluate_list(expr, env):
    l = []
    # loop through all the values in the expr
    for val in expr:
        l.append(evaluate_datum(val, env))
    return l

def evaluate_vector(expr, env):
    l = []
    # loop through all the values in the expr
    for val in expr:
        l.append(evaluate_datum(val, env))
    return l

'''
Do we need to account for environments within lambdas?
We should, but then how do we deal with these??


what is the purpose of the ABBREV token, and how can we differentiate this token from QUOTE, or something else of that nature???
in our interpreter, both essentially do the same thing I believe, just with different syntax...
But quotation does disable evaluation.
Which is already implied by our interpreter, so don't worry about it for now.
Essentially they are equivalent
We may need to rethink how we parse vectors and lists for sake of clairty
'''